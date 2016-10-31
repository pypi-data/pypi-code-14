# Copyright 2014-2016 Morgan Delahaye-Prat. All Rights Reserved.
#
# Licensed under the Simplified BSD License (the "License");
# you may not use this file except in compliance with the License.
"""SQLite3 Model.

The SQLite3 model is a basic model for data persistence with nearly no features
based and solely on the sqlite3 module included in the standard library of
python.
"""


import uuid
import pickle
import sqlite3
from collections import defaultdict
from hypr.helpers.mini_dsl import normalize_query
from hypr.models.exc import ModelInvalidOperation, ModelConflictException, \
    ModelConsistencyException
from hypr.models.base import BaseModel
from hypr.globals import LocalStorage, current_app


locals = LocalStorage()


class _ModelType(type):
    # Perform some class attribute initialization.
    def __new__(mcs, name, bases, d):
        cls = type.__new__(mcs, name, bases, d)
        cls._conn = None
        cls._state = []
        cls._tablename = cls.__tablename__ or cls.__name__.lower()
        cls.__key__ = 'id'
        return cls


class SQLiteModel(BaseModel, metaclass=_ModelType):
    """A model storing its instances in an SQLite3 database.

    The SQLiteModel provides all the basic persistence mechanisms to store and
    retrieve the instances of it. An optimistic concurrency control comes along
    to avoid unwanted overwriting or deletion when multiple agents try to
    perform concurrent operations.

    Any writing operation is performed in a transaction context which must be
    committed or rollbacked. When an operation is done in a request context, it
    has its own transaction context.

    The key of the model is hard-coded to be 'id'.

    The SQLiteModel is a simple yet not secure model and is not intended for
    production.

    Attributes:
        __tablename__: the name of the table used to store the model instances.
    """

    __tablename__ = None
    __filterable__ = 'id',

    @classmethod
    def _filters(cls, **kwargs):
        # process the submitted filters
        query = []
        ordered_params = []
        disjunctions = defaultdict(list)

        # ensure the filterable properties are a tuple
        filterable = cls.__filterable__
        if not isinstance(filterable, tuple):   # pragma: no cover
            filterable = filterable,

        # reorder the query by disjunction groups and check for unknown filters
        for key, values in kwargs.items():
            for positive, value, group in values:
                if key not in filterable:
                    err_msg = '%s: the property is not filterable.'
                    raise ModelInvalidOperation(err_msg % key)
                disjunctions[group].append((positive, key, value))

        for group in disjunctions.values():     # for each disjunction group
            propositions = []
            for positive, key, value in group:  # for each proposition

                range_ = []
                range_val = []

                start = getattr(value, 'start', None)
                stop = getattr(value, 'stop', None)

                if start is not None and positive:
                    range_.append('%s >= ?' % key)
                    range_val.append(start)
                elif start is not None:
                    range_.append('%s < ?' % key)
                    range_val.append(start)

                if stop is not None and positive:
                    range_.append('%s < ?' % key)
                    range_val.append(stop)
                elif stop is not None:
                    range_.append('%s >= ?' % key)
                    range_val.append(stop)

                if range_ and positive:
                    propositions.append('(%s)' % ' AND '.join(range_))
                    ordered_params += range_val
                elif range_:
                    propositions.append('(%s)' % ' OR '.join(range_))
                    ordered_params += range_val
                elif positive:
                    propositions.append('%s = ?' % key)
                    ordered_params.append(value)
                else:
                    propositions.append('%s != ?' % key)
                    ordered_params.append(value)

            query.append('(%s)' % ' OR '.join(propositions))
        return ' AND '.join(query), tuple(ordered_params)

    @classmethod
    def _get_new_connection(cls):
        uri = None
        try:
            uri = current_app.config.get('MODELS_SQLITE_DATABASE_URI')
        except AttributeError:  # pragma: no cover
            pass    # no Hypr app is initialized yet

        if uri is None:
            uri = 'file:/dev/null?mode=memory&cache=shared'
        return sqlite3.connect(uri, uri=True)

    @classmethod
    def conn(cls):
        """Get a connection to a database.

        The connection acts as a transaction context and is bound to the
        request context if there is one. If not, the connection is associated
        to the very model.

        When the connection is established for the first time, the required
        tables are created if necessary.

        Returns:
            A SQLite database connection.
        """
        if cls._conn is None:   # Initialize table if necessary
            cls._conn = cls._get_new_connection()
            c = cls._conn.cursor()

            q = '''CREATE TABLE IF NOT EXISTS %s
                   (id INTEGER PRIMARY KEY, rev TEXT, obj BLOB)'''
            c.execute(q % cls._tablename)
            cls._conn.commit()

        try:
            conn = locals.get('_sqlite_local_connection', None)
            if conn is None:
                conn = cls._get_new_connection()
                locals.set('_sqlite_local_connection', conn)
            return conn
        except RuntimeError:
            pass

        return cls._conn

    @classmethod
    def _clear_state(cls, update):
        # update pending instances and clear state
        try:
            state = locals.get('_sqlite_%s_state' % cls.__name__, [])
        except RuntimeError:
            state = cls._state

        while state:
            instance = state.pop(0)  # pop the data FIFO style

            if update and hasattr(instance, '_pending_id'):
                setattr(instance, '_id', instance._pending_id)
                del instance._pending_id
            if update and hasattr(instance, '_pending_rev'):
                setattr(instance, '_rev', instance._pending_rev)
                del instance._pending_rev

    def _set_pending(self, id_, rev):
        # mark an instance as pending.
        setattr(self, '_pending_id', id_)
        setattr(self, '_pending_rev', rev)

        name = self.__class__.__name__
        try:
            state = locals.get('_sqlite_%s_state' % name, [])
        except RuntimeError:
            state = self._state

        state.append(self)

        try:
            state = locals.set('_sqlite_%s_state' % name, state)
        except RuntimeError:
            pass

    @property
    def id(self):
        """The resource id."""
        return getattr(self, '_id', None)

    @property
    def rev(self):
        """The last known revision."""
        return getattr(self, '_rev', None)

    # CRUD METHODS

    @classmethod
    def get(cls, _offset=0, _limit=-1, **kwargs):
        """Get a list of instances."""
        # ensure the filters (kwargs) are in the mini query DSL format
        for k, v in kwargs.items():
            kwargs[k] = normalize_query(v)

        query = 'SELECT id, rev, obj FROM %s' % cls._tablename

        # apply condition for filtering
        conditions, params = cls._filters(**kwargs)
        if params:
            query += ' WHERE ' + conditions
        query += ' LIMIT ?,?'

        c = cls.conn().cursor()
        c.execute(query, params + (_offset, _limit,))

        rv = []
        for _id, rev, blob in c.fetchall():
            obj = pickle.loads(blob)
            setattr(obj, '_id', _id)
            setattr(obj, '_rev', rev)
            rv.append(obj)

        return rv

    def save(self, commit=True):
        """Mark the instance as to be saved.

        Args:
            commit: Perform a commit at the same time.

        Returns: itself.
        """
        c = self.conn().cursor()

        obj = pickle.dumps(self)
        rev = str(uuid.uuid4())  # update revision

        if self.rev is None:
            query = 'INSERT INTO %s (rev, obj) VALUES (?, ?)'
            c.execute(query % self._tablename, (rev, obj))
        else:
            # before updating, check if the object exists
            query = 'SELECT * FROM %s WHERE id = ?'
            if not c.execute(query % self._tablename, (self.id,)).fetchone():
                raise ModelInvalidOperation('instance not found')

            query = 'UPDATE %s SET rev = ?, obj = ? WHERE rev = ? AND id = ?'
            c.execute(query % self._tablename, (rev, obj, self.rev, self.id))

            # OCC check
            if c.rowcount == 0:
                raise ModelConflictException('outdated instance revision')

        self._set_pending(c.lastrowid or self.id, rev)
        if commit:
            self.commit()

        return self

    def delete(self, commit=True):
        """Mark the instance as to be deleted.

        Args:
            commit: Perform a commit at the same time.

        Returns: itself.
        """
        c = self.conn().cursor()
        name = self.__class__.__name__

        # check if the instance is persistent or pending
        if self.id is None and getattr(self, '_pending_id', None) is None:
            raise ModelInvalidOperation('instance not found')

        # select the most up-to-date known id and revision
        instance_id = self.id or self._pending_id
        instance_rev = self.rev or self._pending_rev

        # check if the instance is known
        query = 'SELECT * FROM %s WHERE id = ?'
        if not c.execute(query % self._tablename, (instance_id,)).fetchone():
            raise ModelInvalidOperation('instance not found')

        # delete matching id/rev
        query = 'DELETE FROM %s WHERE id = ? AND rev = ?'
        c.execute(query % self._tablename, (instance_id, instance_rev))
        if c.rowcount == 0:
            raise ModelConflictException('outdated instance revision')

        self._set_pending(None, None)
        if commit:
            self.commit()

        return self

    @classmethod
    def commit(cls):
        """Commit changes."""
        cls.conn().commit()
        cls._clear_state(update=True)

    @classmethod
    def rollback(cls):
        """Rollback changes."""
        cls.conn().rollback()
        cls._clear_state(update=False)
