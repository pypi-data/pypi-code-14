#!/usr/bin/env python
import datetime
import logging
import multiprocessing
import os

import celery

import shinkansen
from shinkansen import config, db, orm


NULL_SENTINEL = '{[<NULL>]}'


log = logging.getLogger(__name__)


if config.QUEUE_SYSTEM == 'celery':
    celery_app = celery.Celery(
        'shinkansen.worker', broker=config.CELERY_BROKER, config_source=config)
else:
    celery_app = None


queue_migration_queue = {}
# TODO(jpatrin): Add queueing and export queues for other data sources (crate)
for _source_shard in config.MYSQL_SHARDS:
    queue_migration_queue[_source_shard] = multiprocessing.JoinableQueue()
# TODO(jpatrin):Separate stream queues per stream type?
stream_queue = multiprocessing.JoinableQueue()
archive_queue = multiprocessing.JoinableQueue()

# TODO(jpatrin): Need import queues per-shard for mysql
# TODO(jpatrin): Perhaps combine export and import queues/tasks so that we limit the number
# of total queries we're running on each shard.
import_queue = multiprocessing.JoinableQueue()

shutdown_export_event = multiprocessing.Event()
shutdown_stream_event = multiprocessing.Event()
shutdown_import_event = multiprocessing.Event()


class Error(shinkansen.Error):
    pass


class UnrecoverableError(Error, shinkansen.UnrecoverableError):
    pass


class CommandException(Error):
    pass


class RetryException(Exception):
    pass


DATA_TYPE_EXTENSIONS = {'mysql': 'csv', 'crate': 'json'}
SOURCE_DIR = os.path.join(config.TMP_DIR, 'source')
DESTINATION_DIR = os.path.join(config.TMP_DIR, 'destination')
BACKUP_DIR = os.path.join(config.TMP_DIR, 'backup')


def generate_where(conn, chunk_config, table_config):
    where_clauses = []
    where_values = []
    # All of the where clauses generated here will be used by all workers
    if config.INLINE_TRIMMING and table_config.trim_column is not None and table_config.trim_timedelta is not None:
        trim_time = datetime.datetime.now() - table_config.trim_timedelta
        where_clauses = ["%s >= %%(?)s" % (table_config.trim_column,)]
        where_values = [trim_time.strftime(db.TIMESTAMP_FORMAT)]

    if chunk_config.partition_val != 'ALL':
        where_clauses.append('%s = %%(?)s' % (table_config.partition_col,))
        where_values.append(chunk_config.partition_val)

    if chunk_config.migration_type == orm.MigrationType.DELTA:
        where_clauses.append("%s >= %%(?)s" % (table_config.delta_col,))
        where_values.append(conn.from_unixtime_value(chunk_config.delta_start))
        if chunk_config.delta_end is not None:
            where_clauses.append("%s < %%(?)s" % (table_config.delta_col,))
            where_values.append(conn.from_unixtime_value(chunk_config.delta_end))

    elif chunk_config.migration_type != orm.MigrationType.FULL:
        raise UnrecoverableError('Migration type %r unknown' % (chunk_config.migration_type,))

    return (where_clauses, where_values)


class ChunkConfig(object):
    def __init__(
        self,
        migration_id,
        table_config, columns,
        partition_val, namespace, source_shard, destination_shard,
        chunk_num, start_id, chunk_size,
        source_schema=None, destination_schema=None,
        migration_type=orm.MigrationType.FULL,
        delta_start=None, delta_end=None,
        chunk_migration_type=orm.ChunkMigrationType.INDIRECT
    ):
        self.migration_id = migration_id

        self.table_config = table_config

        self.columns = columns

        self.partition_val = partition_val
        self.namespace = namespace
        self.source_shard = source_shard
        self.destination_shard = destination_shard
        self.chunk_num = chunk_num

        self.start_id = start_id
        self.chunk_size = chunk_size
        self.migration_type = migration_type
        self.chunk_migration_type = chunk_migration_type
        self.delta_start = delta_start
        self.delta_end = delta_end

        if namespace is not None and len(namespace) > 0:
            self.source_schema = namespace
            self.destination_schema = namespace
        else:
            self.source_schema = config.SOURCES[self.source_shard]['config']['default_schema_name']
            self.destination_schema = config.DESTINATIONS[self.destination_shard]['config']['default_schema_name']
        if source_schema is not None:
            self.source_schema = source_schema
        if destination_schema is not None:
            self.destination_schema = destination_schema

        self.destination_host = None
        self.destination_ssh_port = None

        self.num_records_exported = 0
        self.num_records_converted = 0
        self.num_records_imported = 0

        self.source_type = config.SOURCES[self.source_shard]['type']
        self.destination_type = config.DESTINATIONS[self.destination_shard]['type']

        self.where_clauses = []
        self.where_values = []

        self.set_filenames()

    @property
    def export_columns(self):
        return [col for col in self.columns if not col.ignore] if self.columns is not None else None

    def set_filenames(self):
        if self.table_config is not None:
            self.export_filename = os.path.join(SOURCE_DIR, ('%s_%s.%s_%s_%s.%s' % (
                self.migration_id, self.source_schema, self.table_config.table_name, self.partition_val,
                self.chunk_num, DATA_TYPE_EXTENSIONS[self.source_type])))
            self.import_filename = os.path.join(DESTINATION_DIR, ('%s_%s.%s_%s_%s.%s' % (
                self.migration_id, self.destination_schema, self.table_config.table_name, self.partition_val,
                self.chunk_num, DATA_TYPE_EXTENSIONS[self.destination_type])))
            self.backup_filename = os.path.join(BACKUP_DIR, ('%s_%s.%s_%s_%s.%s' % (
                self.migration_id, self.destination_schema, self.table_config.table_name, self.partition_val,
                self.chunk_num, DATA_TYPE_EXTENSIONS[self.destination_type])))
        else:
            self.export_filename = None
            self.import_filename = None
            self.backup_filename = None

    # This method is needed for the tests, it is not currently used in the runtime
    def __eq__(self, b):
        return (
            self is b
            or (
                b is not None
                and isinstance(b, ChunkConfig)
                and self.table_config == b.table_config
                and self.columns == b.columns
                and self.partition_val == b.partition_val
                and self.namespace == b.namespace
                and self.source_shard == b.source_shard
                and self.destination_shard == b.destination_shard
                and self.chunk_num == b.chunk_num
                and self.start_id == b.start_id
                and self.chunk_size == b.chunk_size
                and self.source_schema == b.source_schema
                and self.destination_schema == b.destination_schema
                and self.migration_type == b.migration_type
                and self.delta_start == b.delta_start
            )
        )

    def __repr__(self):
        return '%s(%r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r)' % (
            self.__class__.__name__,
            self.migration_id,
            self.table_config, self.columns,
            self.partition_val, self.namespace, self.source_shard, self.destination_shard,
            self.chunk_num, self.start_id, self.chunk_size,
            self.source_schema, self.destination_schema,
            self.migration_type, self.delta_start
        )


class BaseChunkWorker(object):
    def __init__(self, chunk_config, redis_conn, log=None):
        self.c = chunk_config
        self.migration = orm.Migration.get(redis_conn, migration_id=self.c.migration_id)
        self.redis_conn = redis_conn
        if self.c.chunk_num is None:
            self.chunk = None
        else:
            self.chunk = orm.Chunk.get(
                redis_conn,
                migration_id=self.c.migration_id,
                partition_val=self.c.partition_val, table_name=self.c.table_config.table_name,
                chunk_num=self.c.chunk_num, namespace=self.c.namespace,
                source_shard=self.c.source_shard, destination_shard=self.c.destination_shard)
            if self.chunk is None:
                raise UnrecoverableError('Could not find chunk record')
        if log is None:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = log

    def _log(self, log_func, msg, args):
        log_func(
            (msg + ' source_shard=%s destination_shard=%s '
             'source_schema=%s destination_schema=%s table_name=%s '
             'partition_val=%r chunk_num=%r start_id=%r chunk_size=%r'),
            *(args + (
                self.c.source_shard, self.c.destination_shard,
                self.c.source_schema, self.c.destination_schema, self.c.table_config.table_name,
                self.c.partition_val, self.c.chunk_num, self.c.start_id, self.c.chunk_size
            ))
        )

    def log_debug(self, msg, *args):
        self._log(self.logger.debug, msg, args)

    def log_info(self, msg, *args):
        self._log(self.logger.info, msg, args)

    def log_warning(self, msg, *args):
        self._log(self.logger.warning, msg, args)

    def log_error(self, msg, *args):
        self._log(self.logger.error, msg, args)

    def log(self, msg, *args):
        self._log(self.logger.info, msg, args)

    def _run(self):
        raise NotImplementedError()

    def run(self):
        try:
            return self._run()
        except:
            if self.chunk is not None:
                self.chunk.status = 'failed'
                self.chunk.update()
            raise


def migration_task_wrapper(cls):
    def migration_task(self, chunk_config):
        try:
            with db.redis_conn() as redis_conn:
                cls(chunk_config, redis_conn).run()
        except (shinkansen.UnrecoverableError, NotImplementedError), exc:
            log.exception('UnrecoverableError running task %s, NOT requeueing %r', cls.__name__, chunk_config)
            raise
        except RetryException:
            raise self.retry()
        except Exception, exc:
            log.exception('Exception running task %s %r', cls.__name__, chunk_config)
            raise self.retry(exc=exc)
    return migration_task
