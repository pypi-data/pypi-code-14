# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import sys

from tornado import gen

from asyncpg import Connection

if sys.version_info[0] >= 3:
    basestring = str

from collections import deque
import time
import datetime
from contextlib import contextmanager

import psycopg2

from tornado.ioloop import IOLoop
from tornado.concurrent import chain_future, Future

from .exceptions import PoolError, PartiallyConnectedError

log = logging.getLogger('asyncpg')


__author__ = 'zhouqi'


def with_transaction(source=None, transaction=True):
    def decorator(func):
        @gen.coroutine
        def inner_func(*args, **kwargs):
            if source is None and len(args) > 0 and 'pool' in dir(args[0]):
                pool = args[0].pool
            elif isinstance(source, Pool):
                pool = source
            else:
                raise Exception()
                # pl = fakepool(source) # did not implement fake pool
            conn = yield pool.getconn()
            assert (not 'conn' in kwargs)
            kwargs['conn'] = conn
            try:
                if not conn.valid:
                    conn.close()
                    yield conn.connect()
                if not transaction:
                    ret = yield func(*args, **kwargs)
                    raise gen.Return(ret)
                else:
                    yield conn.execute('begin')
                    try:
                        ret = yield func(*args, **kwargs)
                    except Exception as ex:
                        exc = sys.exc_info()
                        try:
                            yield conn.execute('rollback')
                        finally:
                            raise ex
                    else:
                        yield conn.execute('commit')
                        raise gen.Return(ret)
            finally:
                pool.putconn(conn)

        return inner_func

    return decorator

class ConnectionContainer(object):
    """
    Helper class that stores connections according to their state
    """
    def __init__(self):
        self.empty()

    def empty(self):
        self.free = deque()
        self.busy = set()
        self.dead = set()
        self.pending = set()
        self.waiting_queue = deque()

    def add_free(self, conn):
        self.pending.discard(conn)
        log.debug("Handling free connection %s", conn.fileno)

        if not self.waiting_queue:
            log.debug("No outstanding requests - adding to free pool")
            conn.last_used_time = time.time()
            self.free.append(conn)
            return

        log.debug("There are outstanding requests - resumed future from waiting queue")
        self.busy.add(conn)
        future = self.waiting_queue.pop()
        future.set_result(conn)

    def add_dead(self, conn):
        log.debug("Adding dead connection")
        self.pending.discard(conn)
        self.dead.add(conn)

        # If everything is dead, abort anything pending.
        if not self.pending:
            self.abort_waiting_queue(Pool.DatabaseNotAvailable("No database connection available"))

    def acquire(self):
        """Occupy free connection"""
        future = Future()
        while True:
            if self.free:
                conn = self.free.pop()
                if conn.valid:
                    self.busy.add(conn)
                else:
                    self.dead.add(conn)
                    continue
                future.set_result(conn)
                log.debug("Acquired free connection %s", conn.fileno)
                return future
            elif self.busy:
                log.debug("No free connections, and some are busy - put in waiting queue")
                self.waiting_queue.appendleft(future)
                return future
            elif self.pending:
                log.debug("No free connections, but some are pending - put in waiting queue")
                self.waiting_queue.appendleft(future)
                return future
            else:
                log.debug("All connections are dead")
                return None

    def release(self, conn):
        log.debug("About to release connection %s", conn.fileno)
        assert conn in self.busy, "Tried to release non-busy connection"
        self.busy.remove(conn)
        if conn.closed:
            self.dead.add(conn)
        else:
            if not conn.valid:
                conn.close()
                self.dead.add(conn)
            else:
                self.add_free(conn)

    def abort_waiting_queue(self, error):
        while self.waiting_queue:
            future = self.waiting_queue.pop()
            future.set_exception(error)

    def close_alive(self):
        for conn in self.busy.union(self.free):
            if not conn.close:
                conn.close()

    def shrink(self, target_size, delay_in_seconds):
        now = time.time()
        while len(self.free) > target_size and now - self.free[0].last_used_time > delay_in_seconds:
            conn = self.free.popleft()
            conn.close()

    @property
    def all_dead(self):
        return not (self.free or self.busy or self.waiting_queue)

    @property
    def total(self):
        return len(self.free) + len(self.busy) + len(self.dead) + len(self.pending)


class ConnectionContainer2(object):
    """
    Helper class that stores connections according to their state
    """
    def __init__(self):
        self.empty()

    def empty(self):
        self.free = deque()
        self.busy = set()
        self.dead = set()
        self.pending = set()
        self.waiting_queue = deque()

    def add_free(self, conn):
        self.pending.discard(conn)
        log.debug("Handling free connection %s", conn.fileno)

        if not self.waiting_queue:
            log.debug("No outstanding requests - adding to free pool")
            conn.last_used_time = time.time()
            self.free.append(conn)
            return

        log.debug("There are outstanding requests - resumed future from waiting queue")
        self.busy.add(conn)
        future = self.waiting_queue.pop()
        future.set_result(conn)

    def add_dead(self, conn):
        log.debug("Adding dead connection")
        self.pending.discard(conn)
        self.dead.add(conn)

        # If everything is dead, abort anything pending.
        if not self.pending:
            self.abort_waiting_queue(Pool.DatabaseNotAvailable("No database connection available"))

    def acquire(self):
        """Occupy free connection"""
        future = Future()
        if self.free:
            conn = self.free.pop()
            self.busy.add(conn)
            future.set_result(conn)
            log.debug("Acquired free connection %s", conn.fileno)
            return future
        elif self.busy:
            log.debug("No free connections, and some are busy - put in waiting queue")
            self.waiting_queue.appendleft(future)
            return future
        elif self.pending:
            log.debug("No free connections, but some are pending - put in waiting queue")
            self.waiting_queue.appendleft(future)
            return future
        else:
            log.debug("All connections are dead")
            return None

    def release(self, conn):
        log.debug("About to release connection %s", conn.fileno)
        assert conn in self.busy, "Tried to release non-busy connection"
        self.busy.remove(conn)
        if conn.closed:
            self.dead.add(conn)
        else:
            self.add_free(conn)

    def abort_waiting_queue(self, error):
        while self.waiting_queue:
            future = self.waiting_queue.pop()
            future.set_exception(error)

    def close_alive(self):
        for conn in self.busy.union(self.free):
            if not conn.closed:
                conn.close()

    def shrink(self, target_size, delay_in_seconds):
        now = time.time()
        while len(self.free) > target_size and now - self.free[0].last_used_time > delay_in_seconds:
            conn = self.free.popleft()
            conn.close()

    @property
    def all_dead(self):
        return not (self.free or self.busy or self.waiting_queue)

    @property
    def total(self):
        return len(self.free) + len(self.busy) + len(self.dead) + len(self.pending)

class Pool(object):
    """
    Asynchronous conntion pool object. All its methods are
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

    :param int size:
        Minimal number of connections to maintain. ``size`` connections will be opened
        and maintained after calling :py:meth:`asyncpg.Pool.connect`.

    :param max_size:
        if not ``None``, the pool size will dynamically grow on demand up to ``max_size``
        open connections. By default the connections will still be maintained even if
        when the pool load decreases. See also ``auto_shrink`` parameter.
    :type max_size: int or None

    :param ioloop:
        Tornado IOloop instance to use. Defaults to Tornado's ``IOLoop.instance()``.

    :param bool raise_connect_errors:
        Whether to raise :py:meth:`asyncpg.PartiallyConnectedError` when failing to
        connect to database during :py:meth:`asyncpg.Pool.connect`.

    :param int reconnect_interval:
        If database server becomes unavailable, the pool will try to reestablish
        the connection. The attempt frequency is ``reconnect_interval``
        milliseconds.

    :param list setsession:
        List of intial sql commands to be executed once connection is established.
        If any of the commands fails, the connection will be closed.
        **NOTE:** The commands will be executed as one transaction block.

    :param bool auto_shrink:
        Garbage-collect idle connections. Only applicable if ``max_size`` was specified.
        Nevertheless, the pool will mainatain at least ``size`` connections.

    :param shrink_delay:
        A connection is declared idle if it was not used for ``shrink_delay`` time period.
        Idle connections will be garbage-collected if ``auto_shrink`` is set to ``True``.
    :type shrink_delay: :py:meth:`datetime.timedelta`

    :param shrink_period:
        If ``auto_shink`` is enabled, this parameter defines how the pool will check for
        idle connections.
    :type shrink_period: :py:meth:`datetime.timedelta`

    .. _Data Source Name: http://en.wikipedia.org/wiki/Data_Source_Name
    .. _parameters: http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS
    .. _psycopg2.extensions.connection: http://initd.org/psycopg/docs/connection.html#connection
    .. _Connection and cursor factories: http://initd.org/psycopg/docs/advanced.html#subclassing-cursor
    """

    def open(source, transaction=True):
        def decorator(func):
            @gen.coroutine
            def innerfunc(*args, **kwargs):
                if isinstance(source, Pool):
                    pl = source
                # else:
                #     pl = fakepool(source)
                print(pl.dsn)
                conn = yield pl.getconn()
                assert (not 'conn' in kwargs)
                kwargs['conn'] = conn
                try:
                    if not transaction:
                        yield conn.connect()
                        ret = yield func(*args, **kwargs)
                        raise gen.Return(ret)
                    else:
                        yield conn.connect()
                        yield conn.execute('begin')
                        try:
                            ret = yield func(*args, **kwargs)
                        except:
                            exc = sys.exc_info()
                            try:
                                yield conn.execute('rollback')
                            finally:
                                raise exc[0], exc[1], exc[2]
                        else:
                            yield conn.execute('commit')
                            raise gen.Return(ret)
                finally:
                    pl.putconn(conn)

            return innerfunc

        return decorator

    class DatabaseNotAvailable(psycopg2.DatabaseError):
        """Raised when Pool can not connect to database server"""

    def __init__(self,
                 dsn,
                 connection_factory=None,
                 cursor_factory=None,
                 size=1,
                 max_size=None,
                 ioloop=None,
                 raise_connect_errors=True,
                 reconnect_interval=100,
                 setsession=(),
                 auto_shrink=False,
                 shrink_delay=datetime.timedelta(minutes=2),
                 shrink_period=datetime.timedelta(minutes=2)
                 ):

        assert size > 0, "The connection pool size must be a number above 0."

        self.size = size
        self.max_size = max_size or size
        assert self.size <= self.max_size, "The connection pool max size must be of at least 'size'."

        self.dsn = dsn
        self.connection_factory = connection_factory
        self.cursor_factory = cursor_factory
        self.raise_connect_errors = raise_connect_errors
        self.reconnect_interval = float(reconnect_interval)/1000  # the parameter is in milliseconds
        self.setsession = setsession

        self.connected = False
        self.closed = False
        self.server_version = None

        self.ioloop = ioloop or IOLoop.instance()

        self.conns = ConnectionContainer()

        self._last_connect_time = 0
        self._no_conn_available_error = self.DatabaseNotAvailable("No database connection available")
        self.shrink_period = shrink_period
        self.shrink_delay = shrink_delay
        self.auto_shrink = auto_shrink
        if auto_shrink:
            self._auto_shrink()

    def _auto_shrink(self):
        self.conns.shrink(self.size, self.shrink_delay.seconds)
        self.ioloop.add_timeout(self.shrink_period, self._auto_shrink)

    def connect(self):
        """
        Returns future that resolves to this Pool object.

        If some connection failed to connect *and* self.raise_connect_errors
        is true, raises :py:meth:`asyncpg.PartiallyConnectedError`.
        """
        future = Future()
        pending = [self.size-1]

        def on_connect(fut):
            if pending[0]:
                pending[0] -= 1
                return
            # all connection attempts are complete
            if self.conns.dead and self.raise_connect_errors:
                ecp = PartiallyConnectedError("%s connection(s) failed to connect" % len(self.conns.dead))
                future.set_exception(ecp)
            else:
                future.set_result(self)
            log.debug("All initial connection requests complete")

        for i in range(self.size):
            self.ioloop.add_future(self._new_connection(), on_connect)

        return future

    def getconn(self):
        """
        Acquire connection from the pool.

        You can then use this connection for subsequent queries.
        Just use ``connection.execute`` instead of ``Pool.execute``.

        Make sure to return connection to the pool by calling :py:meth:`asyncpg.Pool.putconn`,
        otherwise the connection will remain forever busy and you'll starve your pool.

        Returns a future that resolves to the acquired connection object.

        :param boolean ping:
            Whether to ping the connection before returning it by executing :py:meth:`asyncpg.Connection.ping`.
        """
        rv = self.conns.acquire()
        if isinstance(rv, Future):
            self._reanimate_and_stretch_if_needed()
            future = rv
        else:
            # Else, all connections are dead
            future = Future()
            def on_reanimate_done(fut):
                if self.conns.all_dead:
                    future.set_exception(self._no_conn_available_error)
                    return
                f = self.conns.acquire()
                assert isinstance(f, Future)
                chain_future(f, future)

            self.ioloop.add_future(self._reanimate(), on_reanimate_done)

        return future

    def putconn(self, connection):
        """
        Return busy connection back to the pool.

        **NOTE:** This is a synchronous method.

        :param Connection connection:
            Connection object previously returned by :py:meth:`asyncpg.Pool.getconn`.
        """

        self.conns.release(connection)

        if self.conns.all_dead:
            self.conns.abort_waiting_queue(self._no_conn_available_error)

    @contextmanager
    def manage(self, connection):
        """
        Context manager that automatically returns connection to the pool.
        You can use it instead of :py:meth:`asyncpg.Pool.putconn`::

            connection = yield self.db.getconn()
            with self.db.manage(connection):
                cursor = yield connection.execute("BEGIN")
                ...
        """
        assert connection in self.conns.busy, "Can not manage non-busy connection. Where did you get it from?"
        try:
            yield connection
        finally:
            self.putconn(connection)

    def ping(self):
        """
        Make sure this connection is alive by executing SELECT 1 statement -
        i.e. roundtrip to the database.

        See :py:meth:`asyncpg.Connection.ping` for documentation about the
        parameters.
        """
        return self._operate(Connection.ping)

    def execute(self, *args, **kwargs):
        """
        Prepare and execute a database operation (query or command).

        See :py:meth:`asyncpg.Connection.execute` for documentation about the
        parameters.
        """
        return self._operate(Connection.execute, args, kwargs)

    def callproc(self, *args, **kwargs):
        """
        Call a stored database procedure with the given name.

        See :py:meth:`asyncpg.Connection.callproc` for documentation about the
        parameters.
        """
        return self._operate(Connection.callproc, args, kwargs)

    def transaction(self, *args, **kwargs):
        """
        Run a sequence of SQL queries in a database transaction.

        See :py:meth:`asyncpg.Connection.transaction` for documentation about the
        parameters.
        """
        return self._operate(Connection.transaction, args, kwargs)

    def mogrify(self, *args, **kwargs):
        """
        Return a query string after arguments binding.

        **NOTE:** This is NOT a synchronous method (contary to `asyncpg.Connection.mogrify`)
        - it asynchronously waits for available connection. For performance
        reasons, its better to create dedicated :py:meth:`asyncpg.Connection`
        object and use it directly for mogrification, this operation does not
        imply any real operation on the database server.

        See :py:meth:`asyncpg.Connection.mogrify` for documentation about the
        parameters.
        """
        return self._operate(Connection.mogrify, args, kwargs, async=False)

    def register_hstore(self, *args, **kwargs):
        """
        Register adapter and typecaster for ``dict-hstore`` conversions.

        See :py:meth:`asyncpg.Connection.register_hstore` for documentation about
        the parameters. This method has no ``globally`` parameter, because it
        already registers hstore to all the connections in the pool.
        """
        kwargs["globally"] = True
        return self._operate(Connection.register_hstore, args, kwargs)

    def register_json(self, *args, **kwargs):
        """
        Create and register typecasters converting ``json`` type to Python objects.

        See :py:meth:`asyncpg.Connection.register_json` for documentation about
        the parameters. This method has no ``globally`` parameter, because it
        already registers json to all the connections in the pool.
        """
        kwargs["globally"] = True
        return self._operate(Connection.register_json, args, kwargs)

    def close(self):
        """
        Close the connection pool.

        **NOTE:** This is a synchronous method.
        """
        if self.closed:
            raise PoolError('connection pool is already closed')

        self.conns.close_alive()
        self.conns.empty()
        self.closed = True

    def _operate(self, method, args=(), kwargs=None, async=True, keep=False, connection=None):
        kwargs = kwargs or {}
        future = Future()

        retry = []

        def when_available(fut):
            try:
                conn = fut.result()
            except (psycopg2.Error, psycopg2.OperationalError) as error:
                future.set_exc_info(sys.exc_info())
                if retry and not keep:
                    self.putconn(retry[0])
                return

            log.debug("Obtained connection: %s", conn.fileno)
            try:
                future_or_result = method(conn, *args, **kwargs)
            except (psycopg2.Error, psycopg2.OperationalError) as error:
                log.debug("Method failed synchronously")
                return self._retry(retry, when_available, conn, keep, future)

            if not async:
                if not keep:
                    self.putconn(conn)
                future.set_result(future_or_result)
                return

            def when_done(rfut):
                try:
                    result = rfut.result()
                except (psycopg2.Error, psycopg2.OperationalError) as error:
                    log.debug("Method failed Asynchronously")
                    return self._retry(retry, when_available, conn, keep, future)

                if not keep:
                    self.putconn(conn)
                future.set_result(result)

            self.ioloop.add_future(future_or_result, when_done)

        if not connection:
            self.ioloop.add_future(self.getconn(), when_available)
        else:
            f = Future()
            f.set_result(connection)
            when_available(f)
        return future

    def _retry(self, retry, what, conn, keep, future):
        if conn.closed:
            if not retry:
                retry.append(conn)
                self.ioloop.add_future(conn.connect(), what)
                return
            else:
                future.set_exception(self._no_conn_available_error)
        else:
            future.set_exc_info(sys.exc_info())
        if not keep:
            self.putconn(conn)
        return

    def _reanimate(self):
        assert self.conns.dead, "BUG: don't call reanimate when there is no one to reanimate"

        future = Future()

        if self.ioloop.time() - self._last_connect_time < self.reconnect_interval:
            log.debug("Not reconnecting - too soon")
            future.set_result(None)
            return future

        pending = [len(self.conns.dead)-1]

        def on_connect(fut):
            if pending[0]:
                pending[0] -= 1
                return
            future.set_result(None)

        while self.conns.dead:
            conn = self.conns.dead.pop()
            self.ioloop.add_future(self._connect_one(conn), on_connect)

        return future

    def _reanimate_and_stretch_if_needed(self):
        if self.conns.dead:
            self._reanimate()
            return

        if self.conns.total == self.max_size:
            return  # max size reached
        if self.conns.free:
            return  # no point to stretch if there are free connections
        if self.conns.pending:
            if len(self.conns.pending) >= len(self.conns.waiting_queue):
                return  # there are enough outstanding connection requests

        log.debug("Stretching pool")
        self._new_connection()

    def _new_connection(self):
        log.debug("Spawning new connection")
        conn = Connection(self.dsn,
                          connection_factory=self.connection_factory,
                          cursor_factory=self.cursor_factory,
                          ioloop=self.ioloop,
                          setsession=self.setsession)
        return self._connect_one(conn)

    def _connect_one(self, conn):
        future = Future()
        self.conns.pending.add(conn)

        def on_connect(fut):
            try:
                fut.result()
            except (psycopg2.Error, psycopg2.OperationalError) as error:
                self.conns.add_dead(conn)
            else:
                self.conns.add_free(conn)
                self.server_version = conn.server_version
            self._last_connect_time = self.ioloop.time()
            future.set_result(conn)

        self.ioloop.add_future(conn.connect(), on_connect)
        return future

    def _ping_future_connection(self, conn_future):
        ping_future = Future()

        def on_connection_available(fut):
            conn = fut.result()

            def on_ping_done(ping_fut):
                try:
                    ping_fut.result()
                except (psycopg2.Error, psycopg2.OperationalError):
                    if conn.closed:
                        ping_future.set_exception(self._no_conn_available_error)
                    else:
                        ping_future.set_exc_info(sys.exc_info())
                    self.putconn(conn)
                else:
                    ping_future.set_result(conn)

            f = self._operate(Connection.ping, keep=True, connection=conn)
            self.ioloop.add_future(f, on_ping_done)

        self.ioloop.add_future(conn_future, on_connection_available)

        return ping_future

class Pool2(object):
    """
    Asynchronous conntion pool object. All its methods are
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

    :param int size:
        Minimal number of connections to maintain. ``size`` connections will be opened
        and maintained after calling :py:meth:`asyncpg.Pool.connect`.

    :param max_size:
        if not ``None``, the pool size will dynamically grow on demand up to ``max_size``
        open connections. By default the connections will still be maintained even if
        when the pool load decreases. See also ``auto_shrink`` parameter.
    :type max_size: int or None

    :param ioloop:
        Tornado IOloop instance to use. Defaults to Tornado's ``IOLoop.instance()``.

    :param bool raise_connect_errors:
        Whether to raise :py:meth:`asyncpg.PartiallyConnectedError` when failing to
        connect to database during :py:meth:`asyncpg.Pool.connect`.

    :param int reconnect_interval:
        If database server becomes unavailable, the pool will try to reestablish
        the connection. The attempt frequency is ``reconnect_interval``
        milliseconds.

    :param list setsession:
        List of intial sql commands to be executed once connection is established.
        If any of the commands fails, the connection will be closed.
        **NOTE:** The commands will be executed as one transaction block.

    :param bool auto_shrink:
        Garbage-collect idle connections. Only applicable if ``max_size`` was specified.
        Nevertheless, the pool will mainatain at least ``size`` connections.

    :param shrink_delay:
        A connection is declared idle if it was not used for ``shrink_delay`` time period.
        Idle connections will be garbage-collected if ``auto_shrink`` is set to ``True``.
    :type shrink_delay: :py:meth:`datetime.timedelta`

    :param shrink_period:
        If ``auto_shink`` is enabled, this parameter defines how the pool will check for
        idle connections.
    :type shrink_period: :py:meth:`datetime.timedelta`

    .. _Data Source Name: http://en.wikipedia.org/wiki/Data_Source_Name
    .. _parameters: http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PQCONNECTDBPARAMS
    .. _psycopg2.extensions.connection: http://initd.org/psycopg/docs/connection.html#connection
    .. _Connection and cursor factories: http://initd.org/psycopg/docs/advanced.html#subclassing-cursor
    """

    class DatabaseNotAvailable(psycopg2.DatabaseError):
        """Raised when Pool can not connect to database server"""

    def __init__(self,
                 dsn,
                 connection_factory=None,
                 cursor_factory=None,
                 size=1,
                 max_size=None,
                 ioloop=None,
                 raise_connect_errors=True,
                 reconnect_interval=500,
                 setsession=(),
                 auto_shrink=False,
                 shrink_delay=datetime.timedelta(minutes=2),
                 shrink_period=datetime.timedelta(minutes=2)
                 ):

        assert size > 0, "The connection pool size must be a number above 0."

        self.size = size
        self.max_size = max_size or size
        assert self.size <= self.max_size, "The connection pool max size must be of at least 'size'."

        self.dsn = dsn
        self.connection_factory = connection_factory
        self.cursor_factory = cursor_factory
        self.raise_connect_errors = raise_connect_errors
        self.reconnect_interval = float(reconnect_interval)/1000  # the parameter is in milliseconds
        self.setsession = setsession

        self.connected = False
        self.closed = False
        self.server_version = None

        self.ioloop = ioloop or IOLoop.instance()

        self.conns = ConnectionContainer()

        self._last_connect_time = 0
        self._no_conn_available_error = self.DatabaseNotAvailable("No database connection available")
        self.shrink_period = shrink_period
        self.shrink_delay = shrink_delay
        self.auto_shrink = auto_shrink
        if auto_shrink:
            self._auto_shrink()

    def _auto_shrink(self):
        self.conns.shrink(self.size, self.shrink_delay.seconds)
        self.ioloop.add_timeout(self.shrink_period, self._auto_shrink)

    def connect(self):
        """
        Returns future that resolves to this Pool object.

        If some connection failed to connect *and* self.raise_connect_errors
        is true, raises :py:meth:`asyncpg.PartiallyConnectedError`.
        """
        future = Future()
        pending = [self.size-1]

        def on_connect(fut):
            if pending[0]:
                pending[0] -= 1
                return
            # all connection attempts are complete
            if self.conns.dead and self.raise_connect_errors:
                ecp = PartiallyConnectedError("%s connection(s) failed to connect" % len(self.conns.dead))
                future.set_exception(ecp)
            else:
                future.set_result(self)
            log.debug("All initial connection requests complete")

        for i in range(self.size):
            self.ioloop.add_future(self._new_connection(), on_connect)

        return future

    def getconn(self, ping=True):
        """
        Acquire connection from the pool.

        You can then use this connection for subsequent queries.
        Just use ``connection.execute`` instead of ``Pool.execute``.

        Make sure to return connection to the pool by calling :py:meth:`asyncpg.Pool.putconn`,
        otherwise the connection will remain forever busy and you'll starve your pool.

        Returns a future that resolves to the acquired connection object.

        :param boolean ping:
            Whether to ping the connection before returning it by executing :py:meth:`asyncpg.Connection.ping`.
        """
        rv = self.conns.acquire()
        if isinstance(rv, Future):
            self._reanimate_and_stretch_if_needed()
            future = rv
        else:
            # Else, all connections are dead
            future = Future()

            def on_reanimate_done(fut):
                if self.conns.all_dead:
                    future.set_exception(self._no_conn_available_error)
                    return
                f = self.conns.acquire()
                assert isinstance(f, Future)
                chain_future(f, future)

            self.ioloop.add_future(self._reanimate(), on_reanimate_done)

        if not ping:
            return future
        else:
            return self._ping_future_connection(future)

    def putconn(self, connection):
        """
        Return busy connection back to the pool.

        **NOTE:** This is a synchronous method.

        :param Connection connection:
            Connection object previously returned by :py:meth:`asyncpg.Pool.getconn`.
        """

        self.conns.release(connection)

        if self.conns.all_dead:
            self.conns.abort_waiting_queue(self._no_conn_available_error)

    @contextmanager
    def manage(self, connection):
        """
        Context manager that automatically returns connection to the pool.
        You can use it instead of :py:meth:`asyncpg.Pool.putconn`::

            connection = yield self.db.getconn()
            with self.db.manage(connection):
                cursor = yield connection.execute("BEGIN")
                ...
        """
        assert connection in self.conns.busy, "Can not manage non-busy connection. Where did you get it from?"
        try:
            yield connection
        finally:
            self.putconn(connection)

    def ping(self):
        """
        Make sure this connection is alive by executing SELECT 1 statement -
        i.e. roundtrip to the database.

        See :py:meth:`asyncpg.Connection.ping` for documentation about the
        parameters.
        """
        return self._operate(Connection.ping)

    def execute(self, *args, **kwargs):
        """
        Prepare and execute a database operation (query or command).

        See :py:meth:`asyncpg.Connection.execute` for documentation about the
        parameters.
        """
        return self._operate(Connection.execute, args, kwargs)

    def callproc(self, *args, **kwargs):
        """
        Call a stored database procedure with the given name.

        See :py:meth:`asyncpg.Connection.callproc` for documentation about the
        parameters.
        """
        return self._operate(Connection.callproc, args, kwargs)

    def transaction(self, *args, **kwargs):
        """
        Run a sequence of SQL queries in a database transaction.

        See :py:meth:`asyncpg.Connection.transaction` for documentation about the
        parameters.
        """
        return self._operate(Connection.transaction, args, kwargs)

    def mogrify(self, *args, **kwargs):
        """
        Return a query string after arguments binding.

        **NOTE:** This is NOT a synchronous method (contary to `asyncpg.Connection.mogrify`)
        - it asynchronously waits for available connection. For performance
        reasons, its better to create dedicated :py:meth:`asyncpg.Connection`
        object and use it directly for mogrification, this operation does not
        imply any real operation on the database server.

        See :py:meth:`asyncpg.Connection.mogrify` for documentation about the
        parameters.
        """
        return self._operate(Connection.mogrify, args, kwargs, async=False)

    def register_hstore(self, *args, **kwargs):
        """
        Register adapter and typecaster for ``dict-hstore`` conversions.

        See :py:meth:`asyncpg.Connection.register_hstore` for documentation about
        the parameters. This method has no ``globally`` parameter, because it
        already registers hstore to all the connections in the pool.
        """
        kwargs["globally"] = True
        return self._operate(Connection.register_hstore, args, kwargs)

    def register_json(self, *args, **kwargs):
        """
        Create and register typecasters converting ``json`` type to Python objects.

        See :py:meth:`asyncpg.Connection.register_json` for documentation about
        the parameters. This method has no ``globally`` parameter, because it
        already registers json to all the connections in the pool.
        """
        kwargs["globally"] = True
        return self._operate(Connection.register_json, args, kwargs)

    def close(self):
        """
        Close the connection pool.

        **NOTE:** This is a synchronous method.
        """
        if self.closed:
            raise PoolError('connection pool is already closed')

        self.conns.close_alive()
        self.conns.empty()
        self.closed = True

    def _operate(self, method, args=(), kwargs=None, async=True, keep=False, connection=None):
        kwargs = kwargs or {}
        future = Future()

        retry = []

        def when_available(fut):
            try:
                conn = fut.result()
            except (psycopg2.Error, psycopg2.OperationalError) as error:
                future.set_exc_info(sys.exc_info())
                if retry and not keep:
                    self.putconn(retry[0])
                return

            log.debug("Obtained connection: %s", conn.fileno)
            try:
                future_or_result = method(conn, *args, **kwargs)
            except (psycopg2.Error, psycopg2.OperationalError) as error:
                log.debug("Method failed synchronously")
                return self._retry(retry, when_available, conn, keep, future)

            if not async:
                if not keep:
                    self.putconn(conn)
                future.set_result(future_or_result)
                return

            def when_done(rfut):
                try:
                    result = rfut.result()
                except (psycopg2.Error, psycopg2.OperationalError) as error:
                    log.debug("Method failed Asynchronously")
                    return self._retry(retry, when_available, conn, keep, future)

                if not keep:
                    self.putconn(conn)
                future.set_result(result)

            self.ioloop.add_future(future_or_result, when_done)

        if not connection:
            self.ioloop.add_future(self.getconn(ping=False), when_available)
        else:
            f = Future()
            f.set_result(connection)
            when_available(f)
        return future

    def _retry(self, retry, what, conn, keep, future):
        if conn.closed:
            if not retry:
                retry.append(conn)
                self.ioloop.add_future(conn.connect(), what)
                return
            else:
                future.set_exception(self._no_conn_available_error)
        else:
            future.set_exc_info(sys.exc_info())
        if not keep:
            self.putconn(conn)
        return

    def _reanimate(self):
        assert self.conns.dead, "BUG: don't call reanimate when there is no one to reanimate"

        future = Future()

        if self.ioloop.time() - self._last_connect_time < self.reconnect_interval:
            log.debug("Not reconnecting - too soon")
            future.set_result(None)
            return future

        pending = [len(self.conns.dead)-1]

        def on_connect(fut):
            if pending[0]:
                pending[0] -= 1
                return
            future.set_result(None)

        while self.conns.dead:
            conn = self.conns.dead.pop()
            self.ioloop.add_future(self._connect_one(conn), on_connect)

        return future

    def _reanimate_and_stretch_if_needed(self):
        if self.conns.dead:
            self._reanimate()
            return

        if self.conns.total == self.max_size:
            return  # max size reached
        if self.conns.free:
            return  # no point to stretch if there are free connections
        if self.conns.pending:
            if len(self.conns.pending) >= len(self.conns.waiting_queue):
                return  # there are enough outstanding connection requests

        log.debug("Stretching pool")
        self._new_connection()

    def _new_connection(self):
        log.debug("Spawning new connection")
        conn = Connection(self.dsn,
                          connection_factory=self.connection_factory,
                          cursor_factory=self.cursor_factory,
                          ioloop=self.ioloop,
                          setsession=self.setsession)
        return self._connect_one(conn)

    def _connect_one(self, conn):
        future = Future()
        self.conns.pending.add(conn)

        def on_connect(fut):
            try:
                fut.result()
            except (psycopg2.Error, psycopg2.OperationalError) as error:
                self.conns.add_dead(conn)
            else:
                self.conns.add_free(conn)
                self.server_version = conn.server_version
            self._last_connect_time = self.ioloop.time()
            future.set_result(conn)

        self.ioloop.add_future(conn.connect(), on_connect)
        return future

    def _ping_future_connection(self, conn_future):
        ping_future = Future()

        def on_connection_available(fut):
            conn = fut.result()

            def on_ping_done(ping_fut):
                try:
                    ping_fut.result()
                except (psycopg2.Error, psycopg2.OperationalError):
                    if conn.closed:
                        ping_future.set_exception(self._no_conn_available_error)
                    else:
                        ping_future.set_exc_info(sys.exc_info())
                    self.putconn(conn)
                else:
                    ping_future.set_result(conn)

            f = self._operate(Connection.ping, keep=True, connection=conn)
            self.ioloop.add_future(f, on_ping_done)

        self.ioloop.add_future(conn_future, on_connection_available)

        return ping_future