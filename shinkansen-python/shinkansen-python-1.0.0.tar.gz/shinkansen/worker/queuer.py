from copy import deepcopy
from datetime import datetime
import functools
import logging
import math
import time
import uuid

import shinkansen
from shinkansen import config, db, orm, worker, UnrecoverableError
from shinkansen.worker import (
    ChunkConfig, BaseChunkWorker, migration_task_wrapper,
    queue_migration_queue, celery_app,
    pipe, verifier
)
from shinkansen.worker import exporter


log = logging.getLogger(__name__)


# populated at the end of this module
MIGRATE_TASKS = {}


class Error(worker.Error):
    pass


class QueueChunksWorker(BaseChunkWorker):
    def __init__(self, chunk_config, redis_conn):
        super(QueueChunksWorker, self).__init__(chunk_config, redis_conn, log=log)
        self.column_map = {}
        self.min_id = None
        self.max_id = None
        self.num_rows = None
        self.crate_idx = None
        self.table = orm.Table.get(
            redis_conn,
            migration_id=self.c.migration_id,
            partition_val=self.c.partition_val, table_name=self.c.table_config.table_name,
            namespace=self.c.namespace,
            source_shard=self.c.source_shard, destination_shard=self.c.destination_shard)
        if self.table is None:
            raise UnrecoverableError('Could not find table record')
        # Set self.chunk so BaseChunkWorker.run can set the status to failed if we raise an exception
        self.chunk = self.table
        self.num_chunks = None

    # Overridden, no need for chunk values in log lines
    def _log(self, log_func, msg, args):
        log_func(
            (msg + ' source_shard=%s destination_shard=%s '
             'source_schema=%s destination_schema=%s table_name=%s '
             'partition_val=%r'),
            *(args + (
                self.c.source_shard, self.c.destination_shard,
                self.c.source_schema, self.c.destination_schema, self.c.table_config.table_name,
                self.c.partition_val
            ))
        )

    def get_column_metadata(self, conn):
        raise UnrecoverableError('get_column_metadata is unimplemented')

    def get_table_metadata(self):
        with db.shard_connection(self.c.source_shard, read=True) as conn:
            self.table.source_start_time = conn.get_current_timestamp()
            self.table.start_time = int(time.time() * 1000)
            self.table.status = 'in_progress'
            self.table.update()

            self.get_column_metadata(conn)

            self.c.where_clauses, self.c.where_values = worker.generate_where(conn, self.c, self.c.table_config)

            if (
                self.c.migration_type == orm.MigrationType.DELTA
                and self.c.table_config.join
            ):
                # TODO: come up with a different way to do deltas for crate with a join clause. We don't need the chunking if we do it via json export
                if self.c.source_type == 'crate':
                    self.log_error(
                        'The %s table specifies a join clause but joins are not supported for crate due to lack of '
                        'aggregation support for JOIN queries. This table will not have any delta migrations '
                        'performed.',
                        self.c.table_config.table_name
                    )
                    return
                join = self.c.table_config.join % {'schema': self.c.source_schema}
            else:
                join = ''

            sql = (
                'SELECT COUNT(*), MIN(%(chunk_col)s), MAX(%(chunk_col)s) '
                'FROM %(schema)s.%(table)s %(table_alias)s %(join)s %(where)s'
            ) % {
                'chunk_col': self.c.table_config.chunk_col,
                'schema': self.c.source_schema,
                'table': self.c.table_config.table_name,
                'table_alias': self.c.table_config.table_alias,
                # We only need the join clause for delta and direct currently
                'join': join,
                'where': (' WHERE ' + (' AND '.join(self.c.where_clauses))) if self.c.where_clauses else ''
            }
            with db.cursor(conn) as cur:
                cur.execute(sql % {'?': conn.PARAMETER_PLACEHOLDER}, self.c.where_values)
                (self.num_rows, self.min_id, self.max_id) = cur.fetchone()
        self.log('num_rows=%r min_id=%r max_id=%r', self.num_rows, self.min_id, self.max_id)

    def queue_chunks(self):
        self.c.chunk_size = max(
            1,
            int(
                math.ceil(
                    (self.max_id - self.min_id + 1) /
                    math.ceil(float(self.num_rows) / float(config.CHUNK_SIZE)))))

        # Start at -1 and immediately increment it so that, even if we continue below, we always increase the chunk_num
        chunk_num = -1
        for start_id in xrange(self.min_id, self.max_id + 1, self.c.chunk_size):
            chunk_num += 1

            chunk_config = deepcopy(self.c)
            chunk_config.chunk_num = chunk_num
            chunk_config.start_id = start_id
            chunk_config.set_filenames()

            if self.c.migration_type == orm.MigrationType.FULL:
                ttcs = orm.Chunk.get_by_index(
                    self.redis_conn,
                    # TODO(jpatrin): Add start_id and chunk_size?
                    partition_val=chunk_config.partition_val, table_name=chunk_config.table_config.table_name,
                    chunk_num=chunk_config.chunk_num, namespace=chunk_config.namespace,
                    source_shard=chunk_config.source_shard, destination_shard=chunk_config.destination_shard)
                found_ttc = False
                for ttc in ttcs:
                    if (
                        ttc.status in ('imported', 'empty')
                        # If we were passed a latest migration, only take into account chunks from that migration
                        and (self.c.latest_migration_id is None
                             or ttc.migration_id == self.c.latest_migration_id)
                    ):
                        if not self.c.force:
                            self.log('Chunk already %s, not requeueing', ttc.status)
                            found_ttc = True
                            break
                        self.log('Chunk already %s but reimport forced', ttc.status)
                if found_ttc:
                    continue
            ttc = orm.Chunk(self.redis_conn)
            for col in ttc._cols():
                if hasattr(chunk_config, col):
                    setattr(ttc, col, getattr(chunk_config, col))
                elif hasattr(chunk_config.table_config, col):
                    setattr(ttc, col, getattr(chunk_config.table_config, col))
            ttc.queued_time = int(time.time() * 1000)
            ttc.status = 'queued'
            ttc.insert()

            if self.c.migration_type == orm.MigrationType.FULL:
                if self.c.chunk_migration_type == orm.ChunkMigrationType.INDIRECT:
                    exporter.queue_export_chunk(chunk_config)
                elif self.c.chunk_migration_type == orm.ChunkMigrationType.DIRECT:
                    pipe.queue_pipe_chunk(chunk_config)
            elif self.c.migration_type == orm.MigrationType.DELTA:
                pipe.queue_pipe_chunk(chunk_config)
            else:
                raise UnrecoverableError('Unknown migration type %r' % (self.c.migration_type,))
        self.num_chunks = chunk_num + 1

    def _run(self):
        start = datetime.now()
        self.log('Starting table migration queueing')

        self.get_table_metadata()

        self.table.min_id = self.min_id
        self.table.max_id = self.max_id
        self.table.num_records = self.num_rows

        if self.num_rows == 0 or self.num_rows is None:
            self.log('No rows to migrate')
            self.table.end_time = int(time.time() * 1000)
            self.table.status = 'empty'
            self.table.update()

            # If the table is empty, jump straight to the verification so end-of-migration logic is run.
            verifier.queue_verification(self.c)
            return

        self.queue_chunks()

        self.table.end_time = int(time.time() * 1000)
        self.table.status = 'chunks_queued'
        self.table.num_chunks = self.num_chunks
        self.table.chunk_size = self.c.chunk_size
        self.table.update()

        self.log('Finished queueing table migration elapsed=%s', datetime.now() - start)


class QueueChunksWorkerMysql(QueueChunksWorker):
    TIMESTAMP_TYPES = ['timestamp', 'datetime']
    NUMBER_TYPES = {
        'int': int,
        'tinyint': int,
        'timestamp': int,
        'datetime': int,
        'bigint': int,
        'float': float,
    }
    TYPE_MAP = {
        'int': db.ColumnType.INT,
        'tinyint': db.ColumnType.INT,
        'bigint': db.ColumnType.INT,

        'float': db.ColumnType.FLOAT,

        'timestamp': db.ColumnType.TIMESTAMP,
        'datetime': db.ColumnType.TIMESTAMP,
    }

    # TODO: Most of this needs to move to the MysqlWrapper and needs to be in methods such that we can get the correct
    # metadata and SQL with just a column name and type
    def get_column_metadata(self, conn):
        columns = []
        with db.cursor(conn, dictionary=True) as cur:
            cur.execute('DESCRIBE %s.%s' % (self.c.source_schema, self.c.table_config.table_name))
            for column in cur.fetchall():
                alias = '%s.' % (self.c.table_config.table_alias,) if self.c.table_config.table_alias else ''
                base_type = column['Type'].lower().split('(')[0]  # Ignore anything after an opening parenthesis
                col = db.Column(
                    column['Field'],
                    self.TYPE_MAP.get(base_type, db.ColumnType.STRING),
                    column['Key'] == 'PRI',
                    ignore=(column['Field'].lower() in self.c.table_config.ignore_columns),
                    source_alias=alias
                )

                columns.append(col)
                self.column_map[col.lname] = col

        if (
            self.c.migration_type == orm.MigrationType.DELTA
            or self.c.chunk_migration_type == orm.ChunkMigrationType.DIRECT
        ):
            # Check the destination for the primary key columns as well since the schemas may be different
            with db.shard_connection(self.c.destination_shard, read=True) as conn:
                primary_key = conn.get_table_primary_key_columns(
                    self.c.destination_schema,
                    self.c.table_config.table_name
                )
            for col_name in primary_key:
                if col_name.lower() not in self.column_map:
                    raise UnrecoverableError(
                        'Primary key column in destination does not exist in source '
                        'table=%s column=%s source=%s destination=%s' % (
                            self.c.table_config.table_name, col_name, self.c.source_shard, self.c.destination_shard))
                self.column_map[col_name.lower()].is_primary_key = True
        self.c.columns = columns


class QueueChunksWorkerCrate(QueueChunksWorker):
    NUMBER_TYPES = {
        'integer': int,
        'float': float,
        'timestamp': int,
    }
    TYPE_MAP = {
        'long': db.ColumnType.INT,
        'integer': db.ColumnType.INT,
        'float': db.ColumnType.FLOAT,
        'string': db.ColumnType.STRING,
        'timestamp': db.ColumnType.TIMESTAMP,
    }

    # TODO: Most of this needs to move to the CrateWrapper and needs to be in methods such that we can get the correct
    # metadata and SQL with just a column name and type
    def get_column_metadata(self, conn):
        columns = []
        with db.cursor(conn, dictionary=True) as cur:
            cur.execute(
                'SELECT * FROM information_schema.columns WHERE schema_name = %(?)s AND table_name = %(?)s ' % {
                    '?': conn.PARAMETER_PLACEHOLDER
                },
                (self.c.source_schema.lower(), self.c.table_config.table_name.lower())
            )
            column_recs = cur.fetchall()
        pk_cols = set()
        with db.cursor(conn) as cur:
            cur.execute(
                'SELECT constraint_name FROM information_schema.table_constraints '
                'WHERE constraint_type = %(?)s AND schema_name = %(?)s AND table_name = %(?)s' % {
                    '?': conn.PARAMETER_PLACEHOLDER
                },
                ('PRIMARY_KEY', self.c.source_schema.lower(), self.c.table_config.table_name.lower())
            )
            for (constraint_name,) in cur.fetchall():
                # constraint_name is a list of the columns in the key
                for column in constraint_name:
                    pk_cols.add(column.lower())

        for column in column_recs:
            col = db.Column(
                column['column_name'],
                self.TYPE_MAP[column['data_type']],
                column['column_name'].lower() in pk_cols,
                ignore=(column['column_name'].lower() in self.c.table_config.ignore_columns),
            )

            columns.append(col)
            self.column_map[col.lname] = col

        if (
            self.c.migration_type == orm.MigrationType.DELTA
            or self.c.chunk_migration_type == orm.ChunkMigrationType.DIRECT
        ):
            # Check the destination for the primary key columns as well since the schemas may be different
            with db.shard_connection(self.c.destination_shard, read=True) as conn:
                primary_key = conn.get_table_primary_key_columns(
                    self.c.destination_schema,
                    self.c.table_config.table_name
                )
            for col_name in primary_key:
                if col_name.lower() not in self.column_map:
                    raise UnrecoverableError(
                        'Primary key column in destination does not exist in source '
                        'table=%s column=%s source=%s destination=%s' % (
                            self.c.table_config.table_name, col_name, self.c.source_shard, self.c.destination_shard))
                self.column_map[col_name.lower()].is_primary_key = True
        self.c.columns = columns


def _chunk_config(
    migration_id,
    partition_val, namespace, source_shard, destination_shard,
    table_config, force, migration_type, delta_start, chunk_migration_type
):
    if source_shard not in config.SOURCES:
        raise shinkansen.UnrecoverableError('source_shard invalid %r' % (source_shard,))
    if destination_shard not in config.DESTINATIONS:
        raise shinkansen.UnrecoverableError('destination_shard invalid %r' % (destination_shard,))

    chunk_config = ChunkConfig(
        migration_id=migration_id,
        table_config=table_config,
        columns=None,
        partition_val=partition_val,
        namespace=namespace,
        source_shard=source_shard,
        destination_shard=destination_shard,
        chunk_num=None,
        start_id=None,
        chunk_size=None,
        migration_type=migration_type,
        chunk_migration_type=chunk_migration_type,
        delta_start=delta_start
    )
    # Dynamic property we use just for this task
    chunk_config.force = force
    return chunk_config


# TODO(jpatrin): change to use config.SOURCES and move multiprocessing queue here like in verifier.py
if config.QUEUE_SYSTEM == 'multiprocessing':
    def queue_migrate_table(chunk_config):
        queue_migration_queue[
            config.SOURCES[chunk_config.source_shard]['config']['queue_key']
        ].put(chunk_config)

elif config.QUEUE_SYSTEM == 'celery':
    def queue_migrate_table(chunk_config):
        MIGRATE_TASKS[
            config.SOURCES[chunk_config.source_shard]['config']['queue_key']
        ].delay(chunk_config)

    for _source_name, _source_config in config.SOURCES.items():
        _queue_key = _source_config['config']['queue_key']
        if _queue_key in MIGRATE_TASKS:
            continue
        if _source_config['type'] == 'mysql':
            _task_class = QueueChunksWorkerMysql
        elif _source_config['type'] == 'crate':
            _task_class = QueueChunksWorkerCrate
        else:
            raise UnrecoverableError('Source type %r unknown' % (_source_config['type'],))
        MIGRATE_TASKS[_queue_key] = celery_app.task(
            bind=True,
            name='shinkansen.worker.start_migration_' + _queue_key
        )(migration_task_wrapper(
            _task_class
        ))


# TODO(jpatrin): Apparently unused, remove?
def migrate_partition(
    partition_val, base_namespace, base_source_shard, base_destination_shard,
    force=False, requeue=False
):
    start = datetime.now()
    log.info('Migrating partition partition_val=%s shard=%s', partition_val, base_source_shard)
    for _, suffix in config.SHARD_SUFFIXES.items():
        namespace = base_namespace + suffix if base_namespace is not None and len(base_namespace) > 0 else ''
        source_shard = base_source_shard + suffix
        destination_shard = base_destination_shard + suffix
        if source_shard not in config.SOURCES:
            log.warning('Source shard %r is not configured, skipping', source_shard)
            continue
        if destination_shard not in config.DESTINATIONS:
            log.warning('Destination shard %r is not configured, skipping', destination_shard)
            continue
        migrate_partition_shard(
            partition_val, namespace, source_shard, destination_shard, force, requeue,
            migration_type=orm.MigrationType.FULL)
    log.info('Migration queued partition_val=%s shard=%s elapsed=%s', partition_val, source_shard, datetime.now() - start)


def _migrate_partition_shard_table(migration, table_config, latest_migration, requeue, force):
    # NOTE: refactor
    if migration.type == orm.MigrationType.DELTA and table_config.delta_col is None:
        log.warning(
            'Table %s does not have a delta column configured. '
            ' It will not be queued for delta migration' % (table_config.table_name,))
        return None
    chunk_config = _chunk_config(
        migration.migration_id,
        migration.partition_val, migration.namespace, migration.source_shard, migration.destination_shard,
        table_config,
        force,
        migration.type, migration.delta_start,
        migration.chunk_migration_type)

    if latest_migration is None:
        chunk_config.latest_migration_id = None
    else:
        chunk_config.latest_migration_id = latest_migration.migration_id
        # If we got here with a latest migration, requeue is already true or we're a DELTA migration.
        # In either case we need to query the source in order to know if we have chunks to process.
    table = orm.Table(migration._redis)
    table.migration_id = migration.migration_id
    table.partition_val = migration.partition_val
    table.namespace = migration.namespace
    table.source_shard = migration.source_shard
    table.destination_shard = migration.destination_shard
    table.table_name = table_config.table_name
    table.status = 'queued'
    table.verification_status = ''
    table.queued_time = int(time.time() * 1000)
    table.insert()
    queue_migrate_table(chunk_config)
    return table


def _migrate_partition_shard(
    redis_conn,
    partition_val, namespace, source_shard, destination_shard,
    force=False, requeue=False, migration_type=orm.MigrationType.FULL,
    parent_migration_id=None, latest_migration=None, wanted_delta_start=None, wanted_delta_end=None,
    chunk_migration_type=orm.ChunkMigrationType.INDIRECT
):
    if source_shard not in config.SOURCES:
        raise UnrecoverableError('There is no configured source shard named %r' % (source_shard,))
    if destination_shard not in config.DESTINATIONS:
        raise UnrecoverableError('There is no configured destination shard named %r' % (destination_shard,))
    if chunk_migration_type not in orm.ChunkMigrationType.__ALL__:
        raise UnrecoverableError('chunk_migration_type %r is not valid' % (chunk_migration_type,))
    start = datetime.now()
    migration_id = str(uuid.uuid4())
    log.info('Migrating partition shard type=%s chunk_migration_type=%s partition_val=%s source_shard=%s '
             'destination_shard=%s migration_id=%s',
             migration_type, chunk_migration_type, partition_val, source_shard, destination_shard, migration_id)
    tables = {}
    # Allow the last_migration to be passed in so that container migrations (AUTODELTA and COMPLETE) can pass in
    # the last migration before them for the initial sub-migration that is started as part of the container
    # migration. Otherwise, this code will find the container migration, which has only just been inserted, and
    # fail.
    if latest_migration is None:
        latest_migration = orm.Migration.get_latest(
            redis_conn,
            source_shard=source_shard,
            destination_shard=destination_shard,
            partition_val=partition_val
        )
    # If the last migration is not finished we don't want to allow another one to be queued unless the requestor
    # is specifically asking for requeueing (i.e. in the case of a failed migration or one that was stopped
    # mid-way).
    if latest_migration is not None:
        if latest_migration.migration_id == parent_migration_id:
            log.debug('Latest migration is our parent, ignoring')
        elif not requeue:
            if latest_migration.status not in ('finished', 'empty'):
                raise UnrecoverableError(
                    'Latest migration for this partition is not finished '
                    'partition_val=%s source_shard=%s destination_shard=%s '
                    'latest_migration_id=%s latest_migration_status=%s' % (
                        partition_val, source_shard, destination_shard,
                        latest_migration.migration_id, latest_migration.status))
            elif migration_type not in orm.MigrationType.__DELTA_TYPES__:
                raise UnrecoverableError(
                    'An initial migration has already been performed '
                    'partition_val=%s source_shard=%s destination_shard=%s '
                    'latest_migration_id=%s latest_migration_status=%s' % (
                        partition_val, source_shard, destination_shard,
                        latest_migration.migration_id, latest_migration.status))
    if migration_type in orm.MigrationType.__DELTA_TYPES__:
        delta_end = wanted_delta_end

        if wanted_delta_start is not None:
            delta_start = wanted_delta_start
        else:
            found_migrations = orm.Migration.get_by_index(
                redis_conn,
                source_shard=source_shard,
                destination_shard=destination_shard,
                partition_val=partition_val,
            )
            found_migrations.sort(key=lambda m: m.start_time)
            finished_migrations = [m for m in found_migrations if m.status in ('finished', 'empty')]

            if finished_migrations:
                latest_finished_migration = finished_migrations[-1]
                if latest_finished_migration.type in orm.MigrationType.__DELTA_TYPES__:
                    # Delta on top of delta uses the latest finished delta's source_start_time
                    base_migration = latest_finished_migration
                else:
                    # Delta on top of full migration uses the earlier migration's source_start_time to avoid missing
                    # changes to records that may have been imported before the last finished full migration.
                    base_migration = found_migrations[0]
                # If a delta_end was previously specified, use that as our new delta_start
                if base_migration.delta_end is not None:
                    delta_start = base_migration.delta_end
                elif base_migration.source_start_time:
                    delta_start = (
                        base_migration.source_start_time / 1000 - config.DELTA_START_FUDGE_FACTOR)
                elif base_migration.start_time:
                    log.warning('Base migration did not have a source_start_time, falling back on start_time')
                    delta_start = (
                        base_migration.start_time / 1000 - config.DELTA_START_FUDGE_FACTOR_FALLBACK)
                else:
                    raise UnrecoverableError(
                        'Latest migration does not have a source_start_time, start_time, or delta_end, '
                        'which should not be possible')
                if delta_start is not None and delta_end is not None and delta_end < delta_start:
                    raise UnrecoverableError(
                        'delta_start is after delta_end, this delta migration is nonsensical '
                        'delta_start=%u delta_end=%u' % (delta_start, delta_end))
                log.info('delta_start=%r', delta_start)
            else:
                raise UnrecoverableError(
                    'No finished migration was found for this delta migration to be based on')
    else:
        delta_start = None
        delta_end = None

    migration = orm.Migration(redis_conn)
    migration.type = migration_type
    migration.chunk_migration_type = chunk_migration_type
    migration.migration_id = migration_id
    migration.source_shard = source_shard
    migration.destination_shard = destination_shard
    migration.partition_val = partition_val
    migration.namespace = namespace
    if migration_type in orm.MigrationType.__CONTAINER_TYPES__:
        migration.status = 'in_progress'
    else:
        migration.status = 'queued'
    migration.verification_status = ''
    migration.delta_start = delta_start
    migration.delta_end = delta_end
    migration.parent_migration_id = parent_migration_id
    with db.shard_connection(source_shard, read=True) as conn:
        migration.source_start_time = conn.get_current_timestamp()
    migration.start_time = int(time.time() * 1000)
    migration.insert()
    if migration_type == orm.MigrationType.AUTODELTA:
        # NOTE(jpatrin): We could skip most of the logic above for AUTODELTA since we're going
        # to do it again here for its first DELTA but for now I'd rather leave it in so we don't
        # miss anything.
        _migrate_partition_shard(
            redis_conn,
            partition_val, namespace, source_shard, destination_shard,
            force, requeue, orm.MigrationType.DELTA, migration.migration_id, latest_migration=latest_migration,
            wanted_delta_start=wanted_delta_start, wanted_delta_end=wanted_delta_end,
            chunk_migration_type=chunk_migration_type)
    elif migration_type == orm.MigrationType.COMPLETE:
        _migrate_partition_shard(
            redis_conn,
            partition_val, namespace, source_shard, destination_shard,
            force, requeue, orm.MigrationType.FULL, migration.migration_id,
            chunk_migration_type=chunk_migration_type)
    else:
        for table_config in config.SOURCES[source_shard]['config']['tables']:
            tables[table_config.table_name] = _migrate_partition_shard_table(
                migration, table_config, latest_migration, requeue, force)
    log.info('Migration queued '
             'partition_val=%s source_shard=%s elapsed=%s',
             partition_val, source_shard, datetime.now() - start)
    return (migration, tables)


@functools.wraps(_migrate_partition_shard)
def migrate_partition_shard(
    *args, **kwargs
):
    with db.redis_conn() as redis_conn:
        return _migrate_partition_shard(redis_conn, *args, **kwargs)
