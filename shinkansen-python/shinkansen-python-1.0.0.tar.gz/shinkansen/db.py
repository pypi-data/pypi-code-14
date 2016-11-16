from contextlib import contextmanager
from copy import deepcopy
import datetime
import functools
import logging
import re

import enum

import crate.client
import mysql.connector
import redis.client

import shinkansen
from shinkansen import config
from shinkansen.orm import memredis


log = logging.getLogger(__name__)


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'


class Error(shinkansen.Error):
    pass


def crate_conn(shard_name, *args, **kwargs):
    return crate.client.connect(
        *args,
        servers=[
            '%s:%s' % (node['host'], node['http_port'])
            for node in config.CRATE_SHARDS[shard_name]['client_nodes']
        ],
        **kwargs
    )


@enum.unique
class ColumnType(enum.Enum):
    TIMESTAMP = (1, int)
    INT = (2, int)
    FLOAT = (3, float)
    STRING = (4, str)

    def __init__(self, intvalue, coerce_func):
        self.intvalue = intvalue
        self.coerce_func = coerce_func


class Column(object):
    def __init__(self, name, col_type, is_primary_key, source_alias='', ignore=False):
        self.name = name
        self.type = col_type

        self.lname = name.lower()
        self.is_primary_key = is_primary_key
        self.source_alias = source_alias
        self.ignore = ignore

    def __repr__(self):
        return 'Column(%r, %r, %r, %r, %r)' % (
            self.name, self.type, self.is_primary_key, self.source_alias, self.ignore
        )

    def __eq__(self, b):
        return self is b or (
            b is not None
            and self.name == b.name
            and self.type is b.type
            and self.is_primary_key == b.is_primary_key
            and self.source_alias == b.source_alias
            and self.ignore == b.ignore
        )


class MySQLWrapper(object):
    PARAMETER_PLACEHOLDER = '%s'

    def __init__(self, conn):
        self._conn = conn

    def get_current_timestamp(self):
        with cursor(self._conn) as cur:
            cur.execute('SELECT UNIX_TIMESTAMP(CURRENT_TIMESTAMP()) * 1000')
            return cur.fetchone()[0]

    def get_table_primary_key_columns(self, schema, table):
        with cursor(self._conn) as cur:
            cur.execute(
                '''
                    SELECT k.`COLUMN_NAME`
                    FROM `information_schema`.`TABLE_CONSTRAINTS` t
                    JOIN `information_schema`.`KEY_COLUMN_USAGE` k
                    USING (`CONSTRAINT_NAME`, `TABLE_SCHEMA`, `TABLE_NAME`)
                    WHERE t.`CONSTRAINT_TYPE` = 'PRIMARY KEY'
                    AND t.`TABLE_SCHEMA` = %(?)s
                    AND t.`TABLE_NAME` = %(?)s
                ''' % {
                    '?': self.PARAMETER_PLACEHOLDER
                },
                (schema, table)
            )
            return [k for (k,) in iter(cur.fetchone, None)]

    @staticmethod
    def column_query_sql(col):
        colname = '%s%s' % (col.source_alias, col.name)
        if col.ignore:
            return "''"
        elif col.type == ColumnType.TIMESTAMP:
            return 'UNIX_TIMESTAMP(%s) * 1000' % (colname,)
        else:
            return colname

    @staticmethod
    def column_insert_sql(col):
        if col.type == ColumnType.TIMESTAMP:
            return 'FROM_UNIXTIME(%(?)s / 1000)'
        else:
            return '%(?)s'

    @staticmethod
    def from_unixtime_sql():
        return 'FROM_UNIXTIME(%(?)s)'

    @staticmethod
    def from_unixtime_value(value):
        return datetime.datetime.fromtimestamp(value).strftime(TIMESTAMP_FORMAT)

    @staticmethod
    def from_unixtime(value):
        return 'FROM_UNIXTIME(%u)' % (value,)

    def check_health(self):
        with cursor(self) as cur:
            cur.execute('SELECT 1')
            cur.fetchone()

    def __getattr__(self, name):
        return getattr(self._conn, name)


class CrateDictCursorWrapper(object):
    def __init__(self, cur):
        self._cur = cur
        self._cols = None
        self._orig_next = self._cur.next
        self._cur.next = self.next

    def next(self):
        rec = self._orig_next()
        if self._cols is None:
            self._cols = [col[0] for col in self._cur.description]
        drec = dict(zip(self._cols, rec))
        return drec

    def __getattr__(self, name):
        return getattr(self._cur, name)


class CrateWrapper(object):
    PARAMETER_PLACEHOLDER = '?'

    _CRATE_TABLE_COLUMN_RE = re.compile(r'CREATE TABLE\s+[^(]+\s+\((.*)\n\).*(?:CLUSTERED|WITH)', re.DOTALL)
    _CRATE_COLUMN_RE = re.compile(r'\s*"([^"]+)"\s+(.*)')

    def __init__(self, conn):
        self._conn = conn

    def get_current_timestamp(self):
        with cursor(self._conn) as cur:
            # CURRENT_TIMESTAMP is a crate value. Technically we're not selecting any data from sys.nodes but
            # crate requires a FROM expression in all SQL.
            cur.execute('SELECT CURRENT_TIMESTAMP FROM sys.nodes LIMIT 1')
            return cur.fetchone()[0]

    def get_table_primary_key_columns(self, schema, table):
        with cursor(self._conn) as cur:
            cur.execute(
                '''
                    SELECT constraint_name FROM information_schema.table_constraints
                    WHERE constraint_type = %(?)s AND schema_name = %(?)s AND table_name = %(?)s
                ''' % {
                    '?': self.PARAMETER_PLACEHOLDER
                },
                ('PRIMARY_KEY', schema.lower(), table.lower())
            )
            # this returns a list of columns in the primary key
            pk_cols = cur.fetchone()
        if not pk_cols:
            raise Error('No result checking for primary key of table %s.%s' % (schema, table))
        return pk_cols[0]

    def cursor(self, *args, **kwargs):
        dictionary = kwargs.pop('dictionary', False)
        cur = self._conn.cursor(*args, **kwargs)
        if dictionary:
            cur = CrateDictCursorWrapper(cur)
        return cur

    def get_partition_columns(self, schema, table):
        with cursor(self) as cur:
            cur.execute(
                'SELECT partitioned_by FROM information_schema.tables WHERE schema_name = %(?)s '
                'AND table_name = %(?)s' % {'?': self.PARAMETER_PLACEHOLDER},
                (schema.lower(), table.lower())
            )
            res = cur.fetchone()
            if res is None:
                raise Error('No entry for table %s.%s' % (schema, table))
            if res[0] is None:
                return []
        return res[0]

    def get_unindexed_columns(self, schema, table):
        with cursor(self) as cur:
            unindexed_cols = []
            cur.execute('SHOW CREATE TABLE %s.%s' % (schema, table))
            res = cur.fetchone()
            if res is None:
                raise Error('could not query for unindexed columns')
            create_sql = res[0]
            col_match = self._CRATE_TABLE_COLUMN_RE.match(create_sql)
            if not col_match:
                raise Error('Unable to find columns in CREATE statement: %s' % (create_sql,))
            col_txt = col_match.group(1)
            for line in col_txt.split('\n'):
                if not line or line.strip().startswith('PRIMARY KEY '):
                    continue
                match = self._CRATE_COLUMN_RE.match(line)
                if not match:
                    raise Error('Could not find column in %r' % (line,))
                col = match.group(1)
                if 'INDEX OFF' in match.group(2).upper():
                    unindexed_cols.append(col.lower())
        return unindexed_cols

    def get_unorderable_columns(self, schema, table):
        return set(self.get_partition_columns(schema, table) + self.get_unindexed_columns(schema, table))

    @staticmethod
    def column_query_sql(col):
        if col.ignore:
            return "''"
        else:
            return '%s%s' % (col.source_alias, col.name)

    @staticmethod
    def column_insert_sql(col):
        return '%(?)s'

    @staticmethod
    def from_unixtime_sql():
        return '%(?)s'

    @staticmethod
    def from_unixtime_value(value):
        return datetime.datetime.fromtimestamp(value).strftime(TIMESTAMP_FORMAT)

    @classmethod
    def from_unixtime(cls, value):
        return cls.from_unixtime_value(value)

    def check_health(self):
        with cursor(self) as cur:
            cur.execute('SELECT name FROM sys.cluster')
            cur.fetchone()

    def __getattr__(self, name):
        return getattr(self._conn, name)


@contextmanager
def shard_connection(shard_name, read):
    if shard_name in config.MYSQL_SHARDS:
        mysql_kw = deepcopy(config.MYSQL_SHARDS[shard_name]['read_host' if read else 'write_host'])
        mysql_kw.setdefault('connection_timeout', 600)
        if 'host_type' in mysql_kw:
            del mysql_kw['host_type']
        conn = MySQLWrapper(mysql.connector.connect(**mysql_kw))
    elif shard_name in config.CRATE_SHARDS:
        crate_kw = {
            # This is a query timeout. As such, we need to keep it high to support some of the long queries that we run.
            'timeout': 6000,
        }
        conn = CrateWrapper(crate_conn(shard_name, **crate_kw))
    else:
        raise shinkansen.UnrecoverableError('Unknown shard %r' % (shard_name,))
    exc = False
    try:
        yield conn
    except:
        exc = True
        raise
    finally:
        try:
            conn.close()
        except Exception:
            if exc:
                log.exception(
                    'Exception in finally block while closing connection after an exception has occurred. '
                    'Logging and letting the original exception be raised.')
            else:
                raise


def log_queries(func):
    @functools.wraps(func)
    def wrapper(sql, *a, **k):
        if 'parameters' in k:
            parameters = k['parameters']
        elif len(a) > 0:
            parameters = a[0]
        else:
            parameters = None
        log.debug('Running query sql=%r parameters=%r', sql, parameters)
        return func(sql, *a, **k)
    return wrapper


@contextmanager
def cursor(conn, *args, **kwargs):
    cur = conn.cursor(*args, **kwargs)
    cur.execute = log_queries(cur.execute)
    cur.executemany = log_queries(cur.executemany)
    exc = False
    try:
        yield cur
    except:
        exc = True
        raise
    finally:
        try:
            cur.close()
        except Exception:
            if exc:
                log.exception(
                    'Exception in finally block while closing cursor after an exception has occurred. '
                    'Logging and letting the original exception be raised.')
            else:
                raise


@contextmanager
def shard_cursor(shard_name, read):
    with shard_connection(shard_name, read) as conn:
        with cursor(conn) as cur:
            yield cur


def redis_conn():
    if config.QUEUE_SYSTEM == 'celery':
        return StrictRedis.from_url(config.MIGRATION_REDIS_HOST)
    else:
        return memredis.MemRedis()


# subclassing StrictRedis so we have a close method and can use it as a context manager
class StrictRedis(redis.client.StrictRedis):
    def close(self):
        self.connection_pool.disconnect()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
