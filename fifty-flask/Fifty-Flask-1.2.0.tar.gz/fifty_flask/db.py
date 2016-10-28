import flask_sqlalchemy
import json
from datetime import datetime
from flask import current_app
from sqlalchemy import Column, DateTime, event
from sqlalchemy.ext.declarative.api import declared_attr
from sqlalchemy.ext.mutable import Mutable, MutableDict as DefaultMutableDict
from sqlalchemy.types import TypeDecorator, TEXT
from werkzeug.local import LocalProxy


_db = LocalProxy(lambda: flask_sqlalchemy.get_state(current_app).db)


def full_commit():
    """A convenience function for executing a transaction with automatic
    rollback when an exception occurs. The exception is re-raised.
    """
    try:
        _db.session.commit()
    except:
        _db.session.rollback()
        raise


class ActiveModel(object):
    """A mixin intended to provide convenient functions for repeated SQLAlchemy
    patterns.
    """
    def save(self, commit=True):
        """Adds the current state of the object to the db session and COMMITs
        the transaction if requested.

        Returns a reference to self for convenience
        """
        return self._transact(_db.session.add, commit)

    def delete(self, commit=True):
        """Deletes the object from the databse and COMMITs the transaction
        if requested.
        """
        return self._transact(_db.session.delete, commit)

    def refresh(self):
        """Immediately re-load attributes from the db.
        """
        _db.session.refresh(self)

    def expire(self):
        """Mark the object so that on next access the attributes are refreshed.
        """
        _db.session.expire(self)

    def expunge(self):
        """Remove the instance from the session.
        """
        _db.session.expunge(self)

    def flush(self):
        """Flush all object changes to the database.
        """
        _db.session.flush()

    def column_changed(self, column):
        """Returns True if a column value changed, False otherwise.
        """
        history = self.column_history(column)
        return history.added or history.deleted

    def column_history(self, column):
        """Return the change details for a column.
        """
        return self._sa_instance_state.get_history(column, True)

    def _transact(self, session_fn, commit):
        """Helper for executing an operation on the session and optionally committing.
        """
        session_fn(self)
        
        if commit:
            full_commit()

        return self


class ImmutableJSONEncodedColumn(TypeDecorator):
    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value, **self.get_dumps_kwargs())
        return value

    def get_dumps_kwargs(self):
        return {'separators': (',', ':')}

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value, **self.get_loads_kwargs())
        return value

    def get_loads_kwargs(self):
        return {}


class MutableJSONEncodedColumn(ImmutableJSONEncodedColumn):
    def __init__(self, *args, **kwargs):
        self.null_empty = kwargs.pop('null_empty', False)
        super(MutableJSONEncodedColumn, self).__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if not value and self.null_empty:
            return None
        return super(MutableJSONEncodedColumn, self).process_bind_param(value, dialect)


class JSONEncodedDict(MutableJSONEncodedColumn):
    pass


class MutableDict(DefaultMutableDict):
    def pop(self, *a):
        value = dict.pop(self, *a)
        self.changed()
        return value

    def popitem(self):
        item = dict.popitem(self)
        self.changed()
        return item


MutableDict.associate_with(JSONEncodedDict)


class JSONEncodedList(MutableJSONEncodedColumn):
    pass


class MutableList(Mutable, list):
    def __setitem__(self, index, value):
        list.__setitem__(self, index, value)
        self.changed()

    def append(self, value):
        list.append(self, value)
        self.changed()

    def extend(self, iterable):
        list.extend(self, iterable)
        self.changed()

    def insert(self, index, value):
        list.insert(self, index, value)
        self.changed()

    def pop(self, index=None):
        value = list.pop(self, index)
        self.changed()
        return value

    def remove(self, value):
        list.remove(self, value)
        self.changed()

    def sort(self, *args, **kwargs):
        list.sort(self, *args, **kwargs)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, cls):
            if isinstance(value, list):
                return cls(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __getstate__(self):
        return list(self)

    def __setstate__(self, state):
        self.extend(state)


MutableList.associate_with(JSONEncodedList)


class TimestampedMixin(object):
    """ Mixin to add date created / updated columns to a model.
    """
    @declared_attr
    def date_created(cls):
        return Column(DateTime, default=datetime.utcnow)

    @declared_attr
    def date_updated(cls):
        return Column(DateTime, default=datetime.utcnow)


@event.listens_for(TimestampedMixin, 'before_update', propagate=True)
def timestamped_before_update(mapper, connection, target):
    """ Updates a model with the current time in UTC as the date updated
    """
    target.date_updated = datetime.utcnow()
