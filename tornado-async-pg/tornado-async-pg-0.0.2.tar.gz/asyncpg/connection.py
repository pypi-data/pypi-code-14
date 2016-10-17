# -*- coding: utf-8 -*-
"""
asyncpg.connection
=================

Connection handling.

Copyright 2011-2014, Frank Smit & Zaar Hai.
MIT, see LICENSE for more details.
"""

from __future__ import print_function

import sys
if sys.version_info[0] >= 3:
    basestring = str

import logging
from functools import partial
from collections import deque
import time
import datetime
from functools import wraps
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import register_hstore as _psy_register_hstore
from psycopg2.extras import register_json as _psy_register_json
from psycopg2.extensions import POLL_OK, POLL_READ, POLL_WRITE, POLL_ERROR, TRANSACTION_STATUS_IDLE

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.concurrent import chain_future, Future

from .exceptions import PoolError, PartiallyConnectedError

log = logging.getLogger('asyncpg')

class Connection(object):
    """
    Asynchronous connection object. All its methods are
    asynchronous unless stated otherwide in method description.

    :param string dsn:
        A `Data Source Name`_ string containing one of the following values:

        * **dbname** - the database name
        * **user** - user name used to authenticate
        * **password** - password used to authenticate
        * **host** - database host address (defaults to UNIX socket if not provided)
        * **port** - connection port number (defaults to 5432 if not provided)

        Or any other parameter supported by PostgreSQL. See the PostgreSQL
        documentation for a complete list of supported parameters_.

    :param connection_factory:
        The ``connection_factory`` argument can be used to create non-standard
        connections. The class returned should be a subclass of `psycopg2.extensions.connection`_.
        See `Connection and cursor factories`_ for details. Defaults to ``None``.

    :param cursor_factory:
        The ``cursor_factory`` argument can be used to return non-standart cursor class
        The class returned should be a subclass of `psycopg2.extensions.cursor`_.
        See `Connection and cursor factories`_ for details. Defaults to ``None``.

    :param list setsession:
        List of intial sql commands to be executed once connection is established.
        If any of the commands fails, the connection will be closed.
        **NOTE:** The commands will be executed as one transaction block.

    .. _Data Source Name: http://en.wikipedia.org/wiki/Data_Source_Name
    .. _parameters: http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS
    .. _psycopg2.extensions.connection: http://initd.org/psycopg/docs/connection.html#connection
    .. _Connection and cursor factories: http://initd.org/psycopg/docs/advanced.html#subclassing-cursor
    """
    def __init__(self,
                 dsn,
                 connection_factory=None,
                 cursor_factory=None,
                 ioloop=None,
                 setsession=()):

        self.dsn = dsn
        self.connection_factory = connection_factory
        self.cursor_factory = cursor_factory
        self.ioloop = ioloop or IOLoop.instance()
        self.setsession = setsession

    def connect(self):
        """
        Initiate asynchronous connect.
        Returns future that resolves to this connection object.
        """
        kwargs = {"async": True}
        if self.connection_factory:
            kwargs["connection_factory"] = self.connection_factory
        if self.cursor_factory:
            kwargs["cursor_factory"] = self.cursor_factory

        future = Future()

        self.connection = None
        try:
            self.connection = psycopg2.connect(self.dsn, **kwargs)
        except (psycopg2.Error, psycopg2.OperationalError) as error:
            self.connection = None
            future.set_exc_info(sys.exc_info())
            return future

        self.fileno = self.connection.fileno()

        if self.setsession:
            on_connect_future = Future()

            def on_connect(on_connect_future):
                self.ioloop.add_future(self.transaction(self.setsession), lambda x: future.set_result(self))

            self.ioloop.add_future(on_connect_future, on_connect)
            callback = partial(self._io_callback, on_connect_future, self)
        else:
            callback = partial(self._io_callback, future, self)

        self.ioloop.add_handler(self.fileno, callback, IOLoop.WRITE)
        self.ioloop.add_future(future, self._set_server_version)
        self.ioloop.add_future(future, self._close_on_fail)

        return future

    def _set_server_version(self, future):
        if future.exception():
            return
        self.server_version = self.connection.server_version

    def _close_on_fail(self, future):
        # If connection attempt evetually fails - marks connection as closed by ourselves
        # since psycopg2 does not do that for us (on connection attempts)
        if future.exception():
            self.connection = None

    def _io_callback(self, future, result, fd=None, events=None):
        try:
            state = self.connection.poll()
        except (psycopg2.Warning, psycopg2.Error, psycopg2.OperationalError) as error:
            self.ioloop.remove_handler(self.fileno)
            future.set_exc_info(sys.exc_info())
        else:
            try:
                if state == POLL_OK:
                    self.ioloop.remove_handler(self.fileno)
                    future.set_result(result)
                elif state == POLL_READ:
                    self.ioloop.update_handler(self.fileno, IOLoop.READ)
                elif state == POLL_WRITE:
                    self.ioloop.update_handler(self.fileno, IOLoop.WRITE)
                else:
                    future.set_exception(psycopg2.OperationalError("poll() returned %s" % state))
            except IOError:
                # Can happen when there are quite a lof of outstanding
                # requests. See https://github.com/FSX/momoko/issues/127
                self.ioloop.remove_handler(self.fileno)
                future.set_exception(psycopg2.OperationalError("IOError on socker"))

    def ping(self):
        """
        Make sure this connection is alive by executing SELECT 1 statement -
        i.e. roundtrip to the database.

        Returns future. If it resolves sucessfully - the connection is alive (or dead otherwise).
        """
        return self.execute("SELECT 1 AS ping")

    def execute(self,
                operation,
                parameters=(),
                cursor_factory=None):
        """
        Prepare and execute a database operation (query or command).

        :param string operation: An SQL query.
        :param tuple/list parameters:
            A list or tuple with query parameters. See `Passing parameters to SQL queries`_
            for more information. Defaults to an empty tuple.
        :param cursor_factory:
            The ``cursor_factory`` argument can be used to create non-standard cursors.
            The class returned must be a subclass of `psycopg2.extensions.cursor`_.
            See `Connection and cursor factories`_ for details. Defaults to ``None``.

        Returns future that resolves to cursor object containing result.

        .. _Passing parameters to SQL queries: http://initd.org/psycopg/docs/usage.html#query-parameters
        .. _psycopg2.extensions.cursor: http://initd.org/psycopg/docs/extensions.html#psycopg2.extensions.cursor
        .. _Connection and cursor factories: http://initd.org/psycopg/docs/advanced.html#subclassing-cursor
        """
        kwargs = {"cursor_factory": cursor_factory} if cursor_factory else {}
        cursor = self.connection.cursor(**kwargs)
        cursor.execute(operation, parameters)

        future = Future()
        callback = partial(self._io_callback, future, cursor)
        self.ioloop.add_handler(self.fileno, callback, IOLoop.WRITE)
        return future

    def callproc(self,
                 procname,
                 parameters=(),
                 cursor_factory=None):
        """
        Call a stored database procedure with the given name.

        The sequence of parameters must contain one entry for each argument that
        the procedure expects. The result of the call is returned as modified copy
        of the input sequence. Input parameters are left untouched, output and
        input/output parameters replaced with possibly new values.

        The procedure may also provide a result set as output. This must then be
        made available through the standard `fetch*()`_ methods.

        :param string procname: The name of the database procedure.
        :param tuple/list parameters:
            A list or tuple with query parameters. See `Passing parameters to SQL queries`_
            for more information. Defaults to an empty tuple.
        :param cursor_factory:
            The ``cursor_factory`` argument can be used to create non-standard cursors.
            The class returned must be a subclass of `psycopg2.extensions.cursor`_.
            See `Connection and cursor factories`_ for details. Defaults to ``None``.

        Returns future that resolves to cursor object containing result.

        .. _fetch*(): http://initd.org/psycopg/docs/cursor.html#fetch
        .. _Passing parameters to SQL queries: http://initd.org/psycopg/docs/usage.html#query-parameters
        .. _psycopg2.extensions.cursor: http://initd.org/psycopg/docs/extensions.html#psycopg2.extensions.cursor
        .. _Connection and cursor factories: http://initd.org/psycopg/docs/advanced.html#subclassing-cursor
        """
        kwargs = {"cursor_factory": cursor_factory} if cursor_factory else {}
        cursor = self.connection.cursor(**kwargs)
        cursor.callproc(procname, parameters)

        future = Future()
        callback = partial(self._io_callback, future, cursor)
        self.ioloop.add_handler(self.fileno, callback, IOLoop.WRITE)
        return future

    def mogrify(self, operation, parameters=()):
        """
        Return a query string after arguments binding.

        The string returned is exactly the one that would be sent to the database
        running the execute() method or similar.

        **NOTE:** This is a synchronous method.

        :param string operation: An SQL query.
        :param tuple/list parameters:
            A list or tuple with query parameters. See `Passing parameters to SQL queries`_
            for more information. Defaults to an empty tuple.

        .. _Passing parameters to SQL queries: http://initd.org/psycopg/docs/usage.html#query-parameters
        .. _Connection and cursor factories: http://initd.org/psycopg/docs/advanced.html#subclassing-cursor
        """
        cursor = self.connection.cursor()
        return cursor.mogrify(operation, parameters)

    def transaction(self,
                    statements,
                    cursor_factory=None,
                    auto_rollback=True):
        """
        Run a sequence of SQL queries in a database transaction.

        :param tuple/list statements:
            List or tuple containing SQL queries with or without parameters. An item
            can be a string (SQL query without parameters) or a tuple/list with two items,
            an SQL query and a tuple/list wuth parameters.

            See `Passing parameters to SQL queries`_ for more information.
        :param cursor_factory:
            The ``cursor_factory`` argument can be used to create non-standard cursors.
            The class returned must be a subclass of `psycopg2.extensions.cursor`_.
            See `Connection and cursor factories`_ for details. Defaults to ``None``.
        :param bool auto_rollback:
            If one of the transaction statements fails, try to automatically
            execute ROLLBACK to abort the transaction. If ROLLBACK fails, it would
            not be raised, but only logged.

        Returns future that resolves to ``list`` of cursors. Each cursor contains the result
        of the corresponding transaction statement.

        .. _Passing parameters to SQL queries: http://initd.org/psycopg/docs/usage.html#query-parameters
        .. _psycopg2.extensions.cursor: http://initd.org/psycopg/docs/extensions.html#psycopg2.extensions.cursor
        .. _Connection and cursor factories: http://initd.org/psycopg/docs/advanced.html#subclassing-cursor
        """
        cursors = []
        transaction_future = Future()

        queue = self._statement_generator(statements)

        def exec_statements(future):
            try:
                cursor = future.result()
                cursors.append(cursor)
            except Exception as error:
                if auto_rollback and not self.closed:
                    self._rollback(transaction_future, error)
                else:
                    transaction_future.set_exc_info(sys.exc_info())
                return

            try:
                operation, parameters = next(queue)
            except StopIteration:
                transaction_future.set_result(cursors[1:-1])
                return

            f = self.execute(operation, parameters, cursor_factory)
            self.ioloop.add_future(f, exec_statements)

        self.ioloop.add_future(self.execute("BEGIN;"), exec_statements)
        return transaction_future

    def _statement_generator(self, statements):
        for statement in statements:
            if isinstance(statement, basestring):
                yield (statement, ())
            else:
                yield statement[:2]
        yield ('COMMIT;', ())

    def _rollback(self, transaction_future, error):
        def rollback_callback(rb_future):
            try:
                rb_future.result()
            except Exception as rb_error:
                log.warn("Failed to ROLLBACK transaction %s", rb_error)
            transaction_future.set_exception(error)
        self.ioloop.add_future(self.execute("ROLLBACK;"), rollback_callback)

    def _register(self, future, registrator, fut):
        try:
            cursor = fut.result()
        except Exception as error:
            future.set_exc_info(sys.exc_info())
            return

        oid, array_oid = cursor.fetchone()
        registrator(oid, array_oid)
        future.set_result(None)

    def register_hstore(self, globally=False, unicode=False):
        """
        Register adapter and typecaster for ``dict-hstore`` conversions.

        More information on the hstore datatype can be found on the
        Psycopg2 |hstoredoc|_.

        :param boolean globally:
            Register the adapter globally, not only on this connection.
        :param boolean unicode:
            If ``True``, keys and values returned from the database will be ``unicode``
            instead of ``str``. The option is not available on Python 3.

        Returns future that resolves to ``None``.

        .. |hstoredoc| replace:: documentation

        .. _hstoredoc: http://initd.org/psycopg/docs/extras.html#hstore-data-type
        """
        future = Future()
        registrator = partial(_psy_register_hstore, None, globally, unicode)
        callback = partial(self._register, future, registrator)
        self.ioloop.add_future(self.execute(
            "SELECT 'hstore'::regtype::oid AS hstore_oid, 'hstore[]'::regtype::oid AS hstore_arr_oid",
        ), callback)

        return future

    def register_json(self, globally=False, loads=None):
        """
        Create and register typecasters converting ``json`` type to Python objects.

        More information on the json datatype can be found on the Psycopg2 |regjsondoc|_.

        :param boolean globally:
            Register the adapter globally, not only on this connection.
        :param function loads:
            The function used to parse the data into a Python object.  If ``None``
            use ``json.loads()``, where ``json`` is the module chosen according to
            the Python version.  See psycopg2.extra docs.

        Returns future that resolves to ``None``.

        .. |regjsondoc| replace:: documentation

        .. _regjsondoc: http://initd.org/psycopg/docs/extras.html#json-adaptation
        """
        future = Future()
        registrator = partial(_psy_register_json, None, globally, loads)
        callback = partial(self._register, future, registrator)
        self.ioloop.add_future(self.execute(
            "SELECT 'json'::regtype::oid AS json_oid, 'json[]'::regtype::oid AS json_arr_oid"
        ), callback)

        return future

    @property
    def closed(self):
        """
        Indicates whether the connection is closed or not.
        """
        # 0 = open, 1 = closed, 2 = 'something horrible happened'
        return self.connection.closed > 0 if self.connection else True

    @property
    def valid(self):
        if not self.closed:
            if self.connection.get_transaction_status() == TRANSACTION_STATUS_IDLE:
                return True
        return False

    def close(self):
        """
        Closes the connection.

        **NOTE:** This is a synchronous method.
        """
        if self.connection:
            self.connection.close()


def connect(*args, **kwargs):
    """
    Connection factory.
    See :py:meth:`asyncpg.Connection` for documentation about the parameters.

    Returns future that resolves to :py:meth:`asyncpg.Connection` object or raises exception.
    """
    return Connection(*args, **kwargs).connect()
