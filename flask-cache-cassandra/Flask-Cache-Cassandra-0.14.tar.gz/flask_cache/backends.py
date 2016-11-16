import pickle
from werkzeug.contrib.cache import (BaseCache, NullCache, SimpleCache, MemcachedCache,
                                    GAEMemcachedCache, FileSystemCache)
from ._compat import range_type


class SASLMemcachedCache(MemcachedCache):

    def __init__(self, servers=None, default_timeout=300, key_prefix=None,
                 username=None, password=None):
        BaseCache.__init__(self, default_timeout)

        if servers is None:
            servers = ['127.0.0.1:11211']

        import pylibmc
        self._client = pylibmc.Client(servers,
                                      username=username,
                                      password=password,
                                      binary=True)

        self.key_prefix = key_prefix


class CassandraCache(BaseCache):
    def __init__(self, nodes=None, port=9042, keyspace="flask_cache",
                 table="flask_cache", default_timeout=None,
                 replication_factor=1):
        self.nodes = nodes or []
        self.port = port
        self.keyspace = keyspace
        self.table = table
        self.default_timeout = default_timeout
        self.cluster = Cluster(self.nodes, port=self.port)
        self.cluster.connect().execute(
            """
            CREATE KEYSPACE IF NOT EXISTS {keyspace} WITH replication =
            {{'class': 'SimpleStrategy', 'replication_factor': {factor}}}
            """.format(keyspace=self.keyspace, factor=replication_factor)
        )
        self.session = self.cluster.connect(keyspace=keyspace)
        self._create_table()

    def _create_table(self):
        self.session.execute(
            """
            CREATE TABLE IF NOT EXISTS {table} (
                key text PRIMARY KEY,
                value blob,
            )
            """.format(table=self.table)
        )

    def add(self, key, value, timeout=None):
        if self.has(key):
            return False

        timeout = timeout or self.default_timeout

        if timeout:
            self.session.execute(
                """
                INSERT INTO {table} (key, value) VALUES (%(key)s, %(value)s)
                USING TTL {timeout}
                """.format(table=self.table, timeout=timeout),
                {"key": key, "value": value}
            )
        else:
            self.session.execute(
                """
                INSERT INTO {table} (key, value) VALUES (%(key)s, %(value)s)
                """.format(table=self.table),
                {"key": key, "value": value}
            )

    def clear(self):
        self.session.execute("DROP TABLE {}".format(self.table))
        self._create_table()

    def dec(self, key, delta=1):
        self.session.execute(
            """
            UPDATE {table} SET value = value - %(delta)d WHERE key = %(key)s
            """.format(table=self.table),
            {"key": key, "delta": delta}
        )

    def delete(self, key):
        self.session.execute(
            """
            DELETE FROM {table} WHERE key = %(key)s
            """.format(table=self.table),
            {"key": key},
        )

    def get(self, key):
        rows = self.session.execute(
            """
            SELECT value FROM {table} WHERE key = %(key)s LIMIT 1
            """.format(table=self.table),
            {"key": key}
        )
        for value in rows:
            return pickle.loads(value.value)

    def has(self, key):
        rows = self.session.execute(
            """
            SELECT value FROM {table} WHERE key = %(key)s LIMIT 1
            """.format(table=self.table),
            {"key": key}
        )
        for value in rows:
            return True

        return False

    def inc(self, key, delta=1):
        self.session.execute(
            """
            UPDATE {table} SET value = value + %(delta)d WHERE key = %(key)s
            """.format(table=self.table),
            {"key": key, "delta": delta}
        )

    def set(self, key, value, timeout=None):
        timeout = timeout or self.default_timeout
        if timeout:
            self.session.execute(
                """
                INSERT INTO {table} (key, value) VALUES (%(key)s, %(value)s)
                USING TTL {timeout}
                """.format(table=self.table, timeout=timeout),
                {"key": key, "value": pickle.dumps(value)}
            )
        else:
            self.session.execute(
                """
                INSERT INTO {table} (key, value) VALUES (%(key)s, %(value)s)
                """.format(table=self.table),
                {"key": key, "value": pickle.dumps(value)}
            )


def null(app, config, args, kwargs):
    return NullCache()

def simple(app, config, args, kwargs):
    kwargs.update(dict(threshold=config['CACHE_THRESHOLD']))
    return SimpleCache(*args, **kwargs)

def memcached(app, config, args, kwargs):
    args.append(config['CACHE_MEMCACHED_SERVERS'])
    kwargs.update(dict(key_prefix=config['CACHE_KEY_PREFIX']))
    return MemcachedCache(*args, **kwargs)

def saslmemcached(app, config, args, kwargs):
    args.append(config['CACHE_MEMCACHED_SERVERS'])
    kwargs.update(dict(username=config['CACHE_MEMCACHED_USERNAME'],
                       password=config['CACHE_MEMCACHED_PASSWORD'],
                       key_prefix=config['CACHE_KEY_PREFIX']))
    return SASLMemcachedCache(*args, **kwargs)

def gaememcached(app, config, args, kwargs):
    kwargs.update(dict(key_prefix=config['CACHE_KEY_PREFIX']))
    return GAEMemcachedCache(*args, **kwargs)

def filesystem(app, config, args, kwargs):
    args.insert(0, config['CACHE_DIR'])
    kwargs.update(dict(threshold=config['CACHE_THRESHOLD']))
    return FileSystemCache(*args, **kwargs)

# RedisCache is supported since Werkzeug 0.7.
try:
    from werkzeug.contrib.cache import RedisCache
    from redis import from_url as redis_from_url
except ImportError:
    pass
else:
    def redis(app, config, args, kwargs):
        kwargs.update(dict(
            host=config.get('CACHE_REDIS_HOST', 'localhost'),
            port=config.get('CACHE_REDIS_PORT', 6379),
        ))
        password = config.get('CACHE_REDIS_PASSWORD')
        if password:
            kwargs['password'] = password

        key_prefix = config.get('CACHE_KEY_PREFIX')
        if key_prefix:
            kwargs['key_prefix'] = key_prefix

        db_number = config.get('CACHE_REDIS_DB')
        if db_number:
            kwargs['db'] = db_number

        redis_url = config.get('CACHE_REDIS_URL')
        if redis_url:
            kwargs['host'] = redis_from_url(
                                redis_url,
                                db=kwargs.pop('db', None),
                            )

        return RedisCache(*args, **kwargs)


# Cassandra cache introduced in flask-cache 0.14
try:
    from cassandra.cluster import Cluster
except ImportError:
    pass
else:
    def cassandra(app, config, args, kwargs):
        kwargs.update(dict(
            nodes=config.get('CACHE_CASSANDRA_NODES', ["localhost"]),
            port=config.get('CACHE_CASSANDRA_PORT', 9042),
        ))

        table = config.get('CACHE_CASSANDRA_TABLE')
        if table:
            kwargs['table'] = table

        keyspace = config.get('CACHE_CASSANDRA_KEYSPACE')
        if keyspace:
            kwargs['keyspace'] = keyspace

        replication_factor = config.get('CACHE_CASSANDRA_REPLICATION_FACTOR')
        if replication_factor:
            kwargs['replication_factor'] = replication_factor

        return CassandraCache(*args, **kwargs)


class SpreadSASLMemcachedCache(SASLMemcachedCache):
    """
    Simple Subclass of SASLMemcached client that spread value across multiple
    key is they are bigger than a given treshhold.

    Spreading require using pickle to store the value, wich can significantly
    impact the performances.
    """


    def __init__(self,  *args, **kwargs):
        """
        chunksize : (int) max size in bytes of chunk stored in memcached
        """
        self.chunksize = kwargs.get('chunksize', 950000)
        self.maxchunk = kwargs.get('maxchunk', 32)
        super(SpreadSASLMemcachedCache, self).__init__(*args, **kwargs)

    def delete(self, key):
        for skey in self._genkeys(key):
            super(SpreadSASLMemcachedCache, self).delete(skey)


    def set(self, key, value, timeout=None, chunk=True):
        """set a value in cache, potentially spreding it across multiple key.

        chunk : (Bool) if set to false, does not try to spread across multiple key.
                this can be faster, but will fail if value is bigger than chunks,
                and require you to get back the object by specifying that it is not spread.

        """
        if chunk:
            return self._set(key, value, timeout=timeout)
        else:
            return super(SpreadSASLMemcachedCache, self).set(key, value, timeout=timeout)

    def _set(self, key, value, timeout=None):
        # pickling/unpickling add an overhed,
        # I didn't found a good way to avoid pickling/unpickling if
        # key is smaller than chunksize, because in case or <werkzeug.requests>
        # getting the length consume the data iterator.
        serialized = pickle.dumps(value, 2)
        values = {}
        len_ser = len(serialized)
        chks = range_type(0, len_ser, self.chunksize)
        if len(chks) > self.maxchunk:
            raise ValueError('Cannot store value in less than %s keys'%(self.maxchunk))
        for i in chks:
            values['%s.%s' % (key, i//self.chunksize)] = serialized[i : i+self.chunksize]
        super(SpreadSASLMemcachedCache, self).set_many(values, timeout)

    def get(self, key, chunk=True):
        """get a value in cache, potentially spreded it across multiple key.

        chunk : (Bool) if set to false, get a value set with set(..., chunk=False)
        """
        if chunk :
            return self._get(key)
        else :
            return super(SpreadSASLMemcachedCache, self).get(key)

    def _genkeys(self, key):
        return ['%s.%s' % (key, i) for i in range_type(self.maxchunk)]

    def _get(self, key):
        to_get = ['%s.%s' % (key, i) for i in range_type(self.maxchunk)]
        result = super(SpreadSASLMemcachedCache, self).get_many( *to_get)
        serialized = ''.join([v for v in result if v is not None])
        if not serialized:
            return None
        return pickle.loads(serialized)

def spreadsaslmemcachedcache(app, config, args, kwargs):

    args.append(config['CACHE_MEMCACHED_SERVERS'])
    kwargs.update(dict(username=config.get('CACHE_MEMCACHED_USERNAME'),
                       password=config.get('CACHE_MEMCACHED_PASSWORD'),
                     key_prefix=config.get('CACHE_KEY_PREFIX')
                  ))
    return SpreadSASLMemcachedCache(*args, **kwargs)
