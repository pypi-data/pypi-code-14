__author__ = 'schlitzer'

from random import shuffle
import threading
from pyredis import commands
from pyredis.client import Client, ClusterClient, SentinelClient
from pyredis.exceptions import *
from pyredis.helper import ClusterMap


class BasePool(object):
    """ Base Class for all other pools.

    All other pools inherit from this base class.
    This class itself, cannot be used directly.

    :param database:
        Select which db should be used for this pool
    :type database: int

    :param password:
        Password used for authentication. If None, no authentication is done
    :type password: str

    :param encoding:
        Convert result strings with this encoding. If None, no encoding is done.
    :type encoding: str

    :param conn_timeout:
        Connect Timeout.
    :type conn_timeout: float

    :param read_timeout:
        Read Timeout.
    :type read_timeout: float

    :param pool_size:
        Upper limit of connections this pool can handle.
    :type pool_size: int

    :param lock:
        Class implementing a Lock.
    :type lock: _lock object, defaults to threading.Lock

    """
    def __init__(
            self,
            database=0,
            password=None,
            encoding=None,
            conn_timeout=2,
            read_timeout=2,
            pool_size=16,
            lock=threading.Lock()):
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._lock = lock
        self._pool_free = set()
        self._pool_used = set()
        self._database = database
        self._password = password
        self._encoding = encoding
        self._pool_size = pool_size
        self._close_on_err = False
        self._cluster = False

    @property
    def conn_timeout(self):
        """ Return configured connection timeout

        :return: float
        """
        return self._conn_timeout

    @property
    def read_timeout(self):
        """ Return configured read timeout

        :return: float
        """
        return self._read_timeout

    @property
    def database(self):
        """ Return configured database.

        :return: int
        """
        return self._database

    @property
    def password(self):
        """ Return configured password for this pool.

        :return: str, None
        """
        return self._password

    @property
    def encoding(self):
        """ Return configured encoding

        :return: str, None
        """
        return self._encoding

    @property
    def pool_size(self):
        """ Return, or adjust the current pool size.
        Shrinking the pool is currently not implemented.

        :return: int, None
        """
        return self._pool_size

    @pool_size.setter
    def pool_size(self, size):
        self._pool_size = size

    @property
    def close_on_err(self):
        return self._close_on_err

    def _connect(self):
        raise NotImplemented

    def acquire(self):
        """ Acquire a client connection from the pool.

        :return: redis.Client, exception
        """
        try:
            self._lock.acquire()
            client = self._pool_free.pop()
            self._pool_used.add(client)
        except KeyError:
            if len(self._pool_used) < self.pool_size:
                client = self._connect()
                self._pool_used.add(client)
            else:
                raise PyRedisError('Max connections {0} exhausted'.format(self.pool_size))
        finally:
            self._lock.release()
        return client

    def release(self, conn):
        """ Return a client connection to the pool.

        :param conn:
            redis.Client instance, managed by this pool.
        :return: None
        """
        try:
            self._lock.acquire()
            self._pool_used.remove(conn)
            if conn.closed and self.close_on_err:
                for conn in self._pool_free:
                    conn.close()
                self._pool_free = set()
                self._pool_used = set()
            elif not conn.closed:
                self._pool_free.add(conn)
        except KeyError:
            conn.close()
        finally:
            self._lock.release()


class ClusterPool(
    BasePool,
    commands.Connection,
    commands.Hash,
    commands.HyperLogLog,
    commands.Key,
    commands.List,
    commands.Scripting,
    commands.Set,
    commands.SSet,
    commands.String,
):
    """ Redis Cluster Pool.

    Inherits all the arguments, methods and attributes from BasePool.

    :param seeds:
        Accepts a list of seed nodes in this form: [('host1', 6379), ('host2', 6379), ('host3', 6379)]
    :type sentinels: list

    :param slave_ok:
        Defaults to False. If True, this pool will return connections to slave instances.
    :type slave_ok: bool

    :param retries:
        In case there is a chunk move ongoing, while executing a command, how many times should
        we try to find the right node, before giving up.
    :type retries: int
    """

    def __init__(self, seeds, slave_ok=False, **kwargs):
        super().__init__(**kwargs)
        self._map = ClusterMap(seeds=seeds)
        self._slave_ok = slave_ok
        self._cluster = True

    @property
    def slave_ok(self):
        """ True if this pool will return slave connections

        :return: bool
        """
        return self._slave_ok

    def _connect(self):
        return ClusterClient(
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            slave_ok=self.slave_ok,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout,
            cluster_map=self._map
        )

    def execute(self, *args, **kwargs):
        """ Execute arbitrary redis command.

        :param args:
        :type args: list, int, float

        :return: result, exception
        """
        conn = self.acquire()
        try:
            return conn.execute(*args, **kwargs)
        finally:
            self.release(conn)


class Pool(
    BasePool,
    commands.Connection,
    commands.Hash,
    commands.HyperLogLog,
    commands.Key,
    commands.List,
    commands.Publish,
    commands.Scripting,
    commands.Set,
    commands.SSet,
    commands.String,
):
    """ Pool for straight connections to Redis

    Inherits all the arguments, methods and attributes from BasePool.

    :param host:
        Host IP or Name to connect,
        can only be set when unix_sock is None.
    :type host: str

    :param port:
        Port to connect, only used when host is also set.
    :type port: int

    :param unix_sock:
        Unix Socket to connect,
        can only be set when host is None.
    :type unix_sock: str

    """
    def __init__(self, host=None, port=6379, unix_sock=None, **kwargs):
        if not bool(host) != bool(unix_sock):
            raise PyRedisError("Ether host or unix_sock has to be provided")
        super().__init__(**kwargs)
        self._host = host
        self._port = port
        self._unix_sock = unix_sock

    @property
    def host(self):
        """ Return configured host.

        :return: str, None
        """
        return self._host

    @property
    def port(self):
        """ Return configured port.

        :return: int
        """
        return self._port

    @property
    def unix_sock(self):
        """ Return configured Unix socket.

        :return: str, None
        """
        return self._unix_sock

    def _connect(self):
        return Client(
            host=self.host,
            port=self.port,
            unix_sock=self.unix_sock,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout
            )

    def execute(self, *args):
        """ Execute arbitrary redis command.

        :param args:
        :type args: list, int, float

        :return: result, exception
        """
        conn = self.acquire()
        try:
            return conn.execute(*args)
        finally:
            self.release(conn)


class SentinelPool(
    BasePool,
    commands.Connection,
    commands.Hash,
    commands.HyperLogLog,
    commands.Key,
    commands.List,
    commands.Publish,
    commands.Scripting,
    commands.Set,
    commands.SSet,
    commands.String,
):
    """ Sentinel backed Pool.

    Inherits all the arguments, methods and attributes from BasePool.

    :param sentinels:
        Accepts a list of sentinels in this form: [('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)]
    :type sentinels: list

    :param name:
        Name of the cluster managed by sentinel, that this pool should manage.
    :type name: str

    :param slave_ok:
        Defaults to False. If True, this pool will return connections to slave instances.
    :type slave_ok: bool

    :param retries:
        In case a sentinel delivers stale data, how many other sentinels should be tried.
    :type retries: int
    """
    def __init__(self, sentinels, name, slave_ok=False, retries=3, **kwargs):
        super().__init__(**kwargs)
        self._sentinel = SentinelClient(sentinels=sentinels)
        self._name = name
        self._slave_ok = slave_ok
        self._retries = retries
        self._close_on_err = True

    @property
    def slave_ok(self):
        """ True if this pool return slave connections

        :return: bool
        """
        return self._slave_ok

    @property
    def name(self):
        """ Name of the configured Sentinel managed cluster.

        :return: str
        """
        return self._name

    @property
    def retries(self):
        """ Number of retries in case of stale sentinel.

        :return: int
        """
        return self._retries

    @property
    def sentinels(self):
        """ Deque with configured sentinels.

        :return: deque
        """
        return self._sentinel.sentinels

    def _connect(self):
        for _ in range(self.retries):
            if self.slave_ok:
                client = self._get_slave()
            else:
                client = self._get_master()
            if client:
                return client
        raise PyRedisConnError("Could not connect to Redis")

    def _get_client(self, host, port):
        return Client(
            host=host,
            port=port,
            database=self.database,
            password=self.password,
            encoding=self.encoding,
            conn_timeout=self.conn_timeout,
            read_timeout=self.read_timeout
        )

    def _get_master(self):
        candidate = self._sentinel.get_master(self.name)
        host = candidate[b'ip']
        port = int(candidate[b'port'])
        client = self._get_client(host, port)
        state = client.execute('INFO', 'replication')
        if b'role:master' in state:
            return client
        else:
            client.close()
            self._sentinel.next_sentinel()

    def _get_slave(self):
        candidates = []
        for candidate in self._sentinel.get_slaves(self.name):
            candidates.append((candidate[b'ip'], int(candidate[b'port'])))
        shuffle(candidates)
        for candidate in candidates:
            host = candidate[0]
            port = candidate[1]
            client = self._get_client(host, port)
            state = client.execute('INFO', 'replication')
            if b'role:slave' in state:
                return client
            else:
                client.close()
        self._sentinel.next_sentinel()

    def execute(self, *args):
        """ Execute arbitrary redis command.

        :param args:
        :type args: list, int, float

        :return: result, exception
        """
        conn = self.acquire()
        try:
            return conn.execute(*args)
        finally:
            self.release(conn)
