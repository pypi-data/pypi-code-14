import functools
import logging
from pprint import pformat
import time

import redis.exceptions
import retrying

import shinkansen
from shinkansen import config, lock


log = logging.getLogger(__name__)


RETRY_ORM = True
RETRY_ON_EXCEPTION = True


def retry(*args, **kwargs):
    extra = {}

    def log_exception(exc):
        if RETRY_ON_EXCEPTION:
            log.exception('Got exception, retrying %r %r %r %r', extra['func'], extra['args'], extra['kwargs'], exc)
        return RETRY_ON_EXCEPTION
    kwargs.setdefault('retry_on_exception', log_exception)
    kwargs.setdefault('wait_random_min', 100)
    kwargs.setdefault('wait_random_max', 5000)
    retry_func = retrying.retry(*args, **kwargs)

    def deco(func):
        if not RETRY_ORM:
            return func
        extra['func'] = func

        @functools.wraps(func)
        def capture_func(*args, **kwargs):
            extra['args'] = args
            extra['kwargs'] = kwargs
            return func(*args, **kwargs)
        return retry_func(capture_func)
    return deco


class ORMException(shinkansen.Error):
    pass


class UnrecoverableORMException(shinkansen.UnrecoverableError, ORMException):
    pass


# TODO(jpatrin): Store metadata about:
# TODO(jpatrin): * existing tables
# TODO(jpatrin): * table indices
# These aren't strictly needed as they can be generated trivially from the definitions here


class MultiRedisError(redis.exceptions.RedisError):
    def __init__(self, msg, exceptions):
        super(MultiRedisError, self).__init__(msg)
        self.exceptions = exceptions

    def __repr__(self):
        return super(MultiRedisError, self).__repr__() + ':' + ','.join(repr(e) for e in self.exceptions)

    def __str__(self):
        return super(MultiRedisError, self).__str__() + ':' + ','.join(str(e) for e in self.exceptions)


def raise_redis_exceptions(results):
    exceptions = [result for result in results if isinstance(result, Exception)]
    if len(exceptions) > 0:
        if len(exceptions) == 1:
            raise exceptions[0]
        raise MultiRedisError('Multiple redis exceptions', exceptions)
    return results


# Handles initialization of class-level constants
class DataObjectMeta(type):
    def __init__(cls, name, bases, dct):
        super(DataObjectMeta, cls).__init__(name, bases, dct)
        cls._index_map = {}
        cls._indexed_keys = {}
        if cls._tablename is not None:
            cls._table_records_key = cls._tablename + '||records'
        for index in cls._indexes:
            # always sort index keys so we can look them up easily
            index.sort()
            name = cls._index_name(index)
            cls._index_map[name] = index
            for key in index:
                cls._indexed_keys.setdefault(key, []).append(name)
        for col in cls._key_cols + cls._update_cols:
            cls._column_types.setdefault(col, str)
        cls._key_index_name = cls._index_name(cls._key_cols)


def get_lock(key, redis=None):
    if config.QUEUE_SYSTEM == 'celery':
        return lock.ReentrantRedLock(key + '.LOCK', connection_details=[redis])
    else:
        return lock.ReentrantMemLock(key + '.LOCK')


class DataObject(object):
    __metaclass__ = DataObjectMeta
    _update_cols = []
    _key_cols = []
    _tablename = None
    _indexes = []
    _column_types = {}

    # Populated by DataObjectMeta
    _index_map = None
    _indexed_keys = None
    _table_records_key = None
    _key_index_name = None

    def __init__(self, redis):
        self._redis = redis
        self._reset_dirty()

    def _reset_dirty(self):
        self._dirty_fields = set()
        self._dirty_indexes = {}

    @classmethod
    def _cols(cls):
        return cls._key_cols + cls._update_cols

    def _lock(self, key=None):
        if key is None:
            key = self._key()
        return get_lock(key, self._redis)

    def __setattr__(self, name, value):
        if (
            not name.startswith('_') and
            hasattr(self, name) and
            name not in self._key_cols
        ):
            for index_name in self._indexed_keys.get(name, []):
                if index_name not in self._dirty_indexes:
                    # store the current values for the index so we can move this record to
                    # its new index location when we update
                    self._dirty_indexes[index_name] = {
                        col: getattr(self, col)
                        for col in self._index_map[index_name]
                    }
            self._dirty_fields.add(name)
        return super(DataObject, self).__setattr__(name, value)

    @classmethod
    def _index_name(cls, index):
        return cls.__name__ + '|idx|' + ':'.join(sorted(index))

    def _key(self):
        return self.__class__.__name__ + '|rec|' + ':'.join(
            ('%s=%s' % (col, getattr(self, col))) for col in self._key_cols)

    @classmethod
    def _index_key_values(cls, name, values):
        return '%s=%s' % (name, ','.join(str(values[col]) for col in cls._index_map[name]))

    def _index_key(self, name):
        return '%s=%s' % (name, ','.join(str(getattr(self, col)) for col in self._index_map[name]))

    @classmethod
    def _key_sql(cls):
        return ' AND '.join('"%s"=?' % (col,) for col in cls._key_cols)

    def _key_values(self):
        return [getattr(self, col) for col in self._key_cols]

    def as_dict(self):
        vals = {}
        for col in self._cols():
            val = getattr(self, col)
            if val is not None:
                vals[col] = val
        return vals

    @classmethod
    def from_dict(cls, redis, record):
        obj = cls(redis)
        for col in cls._cols():
            if col not in record or record[col] is None:
                val = None
            else:
                val = cls._column_types[col](record[col])
            setattr(obj, col, val)
        obj._dirty_fields = set()
        obj._dirty_indexes = {}
        return obj

    def copy(self):
        return self.from_dict(self._redis, self.as_dict())

    @classmethod
    def _generate_index(cls, redis, index_name):
        with redis.pipeline() as pipe:
            for rec in cls.get_all(redis):
                rec._add_to_index(index_name, pipe=pipe)
            raise_redis_exceptions(pipe.execute())

    def _add_to_index(self, index_name, pipe=None, key=None):
        if key is None:
            key = self._key()
        if pipe is None:
            pipe = self._redis
        index_key = self._index_key(index_name)
        log.debug('Adding record %r to index %r', key, index_key)
        pipe.sadd(index_key, key)
        pipe.sadd(index_name, index_key)

    def insert(self, lock=None):
        #log.debug('Inserting %r\n%s', self, pformat(self.__dict__))
        key = self._key()
        if lock is None:
            lock = self._lock(key)
        with lock:
            if self._redis.exists(key):
                raise ORMException('Record already exists in redis')
            with self._redis.pipeline() as pipe:
                pipe.hmset(key, self.as_dict())
                for index_name in self._index_map:
                    self._add_to_index(index_name, pipe=pipe, key=key)
                pipe.sadd(self._table_records_key, key)
                results = raise_redis_exceptions(pipe.execute())
            for i in xrange(len(results)):
                if results[i] == 0:
                    if i < 1:
                        continue
                    #if i < len(self._update_cols):
                    #    raise ORMException(
                    #        'Hash value already existed for field %r record %r, possible corrupted record' % (
                    #            self._update_cols[i], key))
                    elif i != len(results) - 1:
                        if (i - 1) % 2 != 0:
                            continue
                        log.warning('Record %r already in redis index %r' % (
                            key, self._index_map.keys()[(i - 1) // 2]))
        self._reset_dirty()

    def update(self, lock=None):
        #log.debug('Updating %r\n%s\n%s\n%s', self, pformat(self.__dict__),
        #          pformat(self._dirty_fields), pformat(self._dirty_indexes))
        if not self._dirty_fields:
            log.warning('Nothing to update')
            return
        key = self._key()
        if lock is None:
            lock = self._lock(key)
        with lock:
            with self._redis.pipeline() as pipe:
                vals = {}
                delfields = []
                for col in self._dirty_fields:
                    val = getattr(self, col)
                    if val is None:
                        delfields.append(col)
                    else:
                        vals[col] = val
                if delfields:
                    pipe.hdel(key, *delfields)
                if vals:
                    pipe.hmset(key, vals)
                dirty_indexes = self._dirty_indexes.items()
                for index_name, old_values in dirty_indexes:
                    index_key = self._index_key(index_name)
                    pipe.smove(
                        self._index_key_values(index_name, old_values),
                        index_key,
                        key
                    )
                    # TODO(jpatrin): Remove old index key if it's empty?
                    pipe.sadd(index_name, index_key)
                results = raise_redis_exceptions(pipe.execute())
            index_results = results[1 + (1 if len(delfields) > 0 else 0):]
            initial_results = (1 if delfields else 0) + (1 if vals else 0)
            for i in xrange(len(index_results)):
                # skip the hdel and hmset responses, we're checking for the index updates
                if i < initial_results:
                    continue
                i -= initial_results
                # These are the bookkeeping entries
                if i % 2 != 0:
                    continue
                if index_results[i] == 0:
                    log.warning('Redis index %r should have had record %r, repairing' % (
                        self._index_key_values(*dirty_indexes[i // 2]), key))
                    index_name = dirty_indexes[i // 2][0]
                    self._redis.sadd(self._index_key(index_name), key)
        self._reset_dirty()

    def delete(self, lock=None):
        #log.debug('Deleting %r\n%s', self, pformat(self.__dict__))
        key = self._key()
        if lock is None:
            lock = self._lock(key)
        with lock:
            with self._redis.pipeline() as pipe:
                pipe.delete(key)
                pipe.srem(self._table_records_key, key)
                for name in self._index_map:
                    pipe.srem(self._index_key(name), key)
                # These could return 0 but we don't really care since we're deleting anyway
                raise_redis_exceptions(pipe.execute())

    @classmethod
    def get_all(cls, redis):
        """
        Generator which yields all records in the table one by one.
        """
        for key in redis.smembers(cls._table_records_key):
            rec = redis.hgetall(key)
            if rec is None:
                log.warning('Record %r does not exist but is listed in the table' % (key,))
                continue
            yield cls.from_dict(redis, rec)

    @classmethod
    def get(cls, redis, **key_values):
        if len(key_values) != len(cls._key_cols) or any(col not in key_values for col in cls._key_cols):
            raise UnrecoverableORMException('You must give only all key columns as keyword arguments to get()')
        obj = cls(redis)

        # TODO(jpatrin): use from_dict?
        for col in cls._key_cols:
            val = cls._column_types[col](key_values[col])
            setattr(obj, col, val)
        values = redis.hgetall(obj._key())
        if not values:
            # TODO(jpatrin): Could be that all of the _update_cols are just empty...
            return None
        for col in cls._update_cols:
            if col in values:
                val = cls._column_types[col](values[col])
            else:
                val = None
            setattr(obj, col, val)
        obj._dirty_fields = set()
        obj._dirty_indexes = {}
        return obj

    def get_self(self):
        return self.get(self._redis, **{col: getattr(self, col) for col in self._key_cols})

    @classmethod
    def get_by_index(cls, redis, **clauses):
        index_name = cls._index_name(clauses.keys())
        # The key (primary key) is a special case
        if index_name == cls._key_index_name:
            rec = cls.get(redis, **clauses)
            if rec:
                return [rec]
            else:
                return []
        if index_name not in cls._index_map:
            raise UnrecoverableORMException('Index for %r is not defined for class %s' % (clauses.keys(), cls.__name__))
        objs = []
        for record_key in redis.smembers(cls._index_key_values(index_name, clauses)):
            record = redis.hgetall(record_key)
            if record is None:
                log.warning('Record %r does not exist but is in index %r' % (record_key, index_name))
                continue
            objs.append(cls.from_dict(redis, record))
        return objs

    @classmethod
    def get_columns(cls, redis, columns=None):
        if columns is None:
            columns = cls._cols()
        with redis.pipeline() as pipe:
            for key in redis.smembers(cls._table_records_key):
                pipe.hmget(key, columns)
            return pipe.execute()

    def __eq__(self, b):
        return (
            b is not None
            and (
                self is b
                or all(
                    getattr(self, col) == getattr(b, col)
                    for col in self._cols()
                )
            )
        )

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join('%s=%r' % (col, getattr(self, col)) for col in self._cols())
        )


class Worker(DataObject):
    _tablename = 'migration.worker'
    _key_cols = ['host', 'pid']
    _update_cols = [
        'partition_val', 'namespace', 'source_shard', 'destination_shard', 'table_name', 'chunk_num',
        'status', 'type', 'last_checkin', 'migration_id']
    _indexes = [
        ['status'],
    ]

    def __init__(self, redis):
        super(Worker, self).__init__(redis)
        self.host = None
        self.pid = None
        self.type = None
        self.partition_val = None
        self.namespace = None
        self.source_shard = None
        self.destination_shard = None
        self.table_name = None
        self.chunk_num = None
        self.status = None
        self.last_checkin = None
        self.migration_id = None

    def update(self):
        self.last_checkin = int(time.time() * 1000)
        super(Worker, self).update()

        log.debug('Self post-update: %s', pformat(self.get_self()))


# TODO(jpatrin): use enum.Enum here, but means making use of .value when writing to DB,
# using Class(value) when reading from the DB
# and using .value when outputting via APIs.
class MigrationType(object):
    # Migration types:
    FULL = 'full'
    DELTA = 'delta'
    AUTODELTA = 'autodelta'
    COMPLETE = 'complete'
    __CONTAINER_TYPES__ = (AUTODELTA, COMPLETE)
    __DELTA_TYPES__ = (DELTA, AUTODELTA)
    __ALL__ = (FULL, DELTA, AUTODELTA, COMPLETE)


class ChunkMigrationType(object):
    INDIRECT = 'indirect'
    DIRECT = 'direct'
    __ALL__ = (DIRECT, INDIRECT)


class Migration(DataObject):
    _tablename = 'migration.migration'
    _key_cols = ['migration_id']
    _update_cols = [
        'type', 'chunk_migration_type',
        'source_shard', 'destination_shard', 'partition_val',
        'namespace', 'status', 'verification_status',
        'source_start_time', 'start_time', 'end_time',
        'delta_start', 'delta_end', 'parent_migration_id']
    _column_types = {
        'start_time': int,
        'end_time': int,
        'source_start_time': int,
        'delta_start': int,
        'delta_end': int,
    }
    _indexes = [
        ['partition_val'],
        ['partition_val', 'source_shard', 'destination_shard'],
        ['source_shard', 'destination_shard', 'partition_val', 'namespace'],
        ['status'],
        ['partition_val', 'type'],
        ['partition_val', 'source_shard', 'destination_shard', 'type'],
        ['source_shard', 'destination_shard', 'partition_val', 'namespace', 'type'],
        ['status', 'type'],
        ['parent_migration_id'],
    ]

    def __init__(self, redis):
        super(Migration, self).__init__(redis)
        self.migration_id = None
        self.type = None
        self.chunk_migration_type = None
        self.source_shard = None
        self.destination_shard = None
        self.partition_val = None
        self.namespace = None
        self.status = None
        self.verification_status = None
        self.source_start_time = None
        self.start_time = None
        self.end_time = None
        self.delta_start = None
        self.delta_end = None
        self.parent_migration_id = None

    @classmethod
    def get_latest(cls, redis_conn, **clauses):
        # TODO(jpatrin): Make this better by creating sorted indices?
        migrations = cls.get_by_index(
            redis_conn,
            **clauses
        )
        if migrations:
            migrations.sort(key=lambda m: m.start_time)
            return migrations[-1]
        else:
            return None

    def get_submigrations(self):
        submigrations = self.get_by_index(self._redis, parent_migration_id=self.migration_id)
        if not submigrations:
            return None
        submigrations.sort(key=lambda m: m.start_time)
        return submigrations

    def get_latest_submigration(self):
        submigrations = self.get_submigrations()
        if not submigrations:
            return None
        return submigrations[-1]


class Table(DataObject):
    _tablename = 'migration.table'
    # should namespace be a key column?
    _key_cols = [
        'migration_id', 'partition_val', 'namespace', 'source_shard', 'destination_shard', 'table_name',
    ]
    _update_cols = [
        'min_id', 'max_id', 'num_records',
        'status', 'chunk_size',
        'queued_time', 'start_time', 'end_time',
        'verification_status',
        'source_start_time',
    ]
    _column_types = {
        'min_id': int,
        'max_id': int,
        'num_records': int,
        'chunk_size': int,
        'queued_time': int,
        'start_time': int,
        'end_time': int,
        'source_start_time': int,
    }
    _indexes = [
        ['partition_val'],
        ['migration_id'],
        ['partition_val', 'table_name'],
        ['partition_val', 'destination_shard', 'source_shard'],
        ['partition_val', 'destination_shard', 'source_shard', 'table_name'],
        ['partition_val', 'namespace', 'source_shard', 'destination_shard', 'table_name'],
        ['status'],
    ]

    def __init__(self, redis):
        super(Table, self).__init__(redis)
        self.migration_id = None
        self.partition_val = None
        self.namespace = None
        self.source_shard = None
        self.destination_shard = None
        self.table_name = None

        self.status = None
        self.verification_status = None

        self.min_id = None
        self.max_id = None
        self.num_records = None
        self.num_chunks = None
        self.chunk_size = None

        self.queued_time = None
        self.source_start_time = None
        self.start_time = None
        self.end_time = None

    def update_status(self, status, where_status):
        lock = self._lock()
        with lock:
            obj = self.get_self()
            if obj.status == where_status:
                obj.status = status
                obj.update(lock=lock)


class Chunk(DataObject):
    _tablename = 'migration.chunk'
    # should namespace be a key column?
    _key_cols = [
        'migration_id', 'partition_val', 'namespace', 'source_shard', 'destination_shard', 'table_name', 'chunk_num'
    ]
    _update_cols = [
        'start_id', 'num_records_exported', 'num_records_converted', 'num_records_imported',
        'destination_host', 'status', 'chunk_size',
        'queued_time', 'start_time', 'end_time', 'export_elapsed_ms', 'convert_elapsed_ms', 'import_elapsed_ms',
    ]
    _column_types = {
        'start_id': int,
        'num_records_exported': int,
        'num_records_converted': int,
        'num_records_imported': int,
        'chunk_size': int,
        'queued_time': int,
        'start_time': int,
        'end_time': int,
        'export_elapsed_ms': int,
        'convert_elapsed_ms': int,
        'import_elapsed_ms': int,
    }
    _indexes = [
        ['partition_val'],
        ['migration_id'],
        ['partition_val', 'source_shard', 'destination_shard'],
        ['partition_val', 'source_shard', 'destination_shard', 'table_name'],
        ['partition_val', 'namespace', 'source_shard', 'destination_shard', 'table_name', 'chunk_num'],
        ['partition_val', 'table_name'],
        ['status'],
    ]

    def __init__(self, redis):
        super(Chunk, self).__init__(redis)
        self.migration_id = None
        self.partition_val = None
        self.namespace = None
        self.source_shard = None
        self.destination_shard = None
        self.table_name = None
        self.chunk_num = None
        self.start_id = None
        self.chunk_size = None
        self.num_records_exported = None
        self.num_records_converted = None
        self.num_records_imported = None
        self.destination_host = None
        self.status = None
        self.queued_time = None
        self.start_time = None
        self.end_time = None
        self.export_elapsed_ms = None
        self.convert_elapsed_ms = None
        self.import_elapsed_ms = None

    def update_status(self, status, where_status):
        _lock = self._lock()
        with _lock:
            obj = self.get_self()
            if obj.status == where_status:
                obj.status = status
                obj.update(lock=_lock)
