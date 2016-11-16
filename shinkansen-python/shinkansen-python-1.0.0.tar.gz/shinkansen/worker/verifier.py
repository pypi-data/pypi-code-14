from datetime import datetime
import logging
import multiprocessing
import time

import redlock.lock

import shinkansen
import shinkansen.worker
from shinkansen import db, orm, status, worker
from shinkansen.worker import (
    # queuer is imported in the code below as if it is imported here it creates an import cycle
    celery_app, migration_task_wrapper,
    BaseChunkWorker, Error
)
from shinkansen import config


log = logging.getLogger(__name__)


TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S'


class VerifyWorker(BaseChunkWorker):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log', log)
        super(VerifyWorker, self).__init__(*args, **kwargs)

    def _log(self, log_func, msg, args):
        if self.c.table_config is not None:
            super(VerifyWorker, self)._log(log_func, msg, args)
        else:
            log_func(
                (msg + ' source_shard=%s destination_shard=%s '
                 'source_schema=%s destination_schema=%s '
                 'partition_val=%r'),
                *(args + (
                    self.c.source_shard, self.c.destination_shard,
                    self.c.source_schema, self.c.destination_schema,
                    self.c.partition_val
                ))
            )

    def check_table(self, table_config, conn):
        table_data = orm.Table.get(
            self.redis_conn,
            migration_id=self.c.migration_id,
            partition_val=self.c.partition_val, namespace=self.c.namespace,
            source_shard=self.c.source_shard, destination_shard=self.c.destination_shard,
            table_name=table_config.table_name)
        if table_data is None:
            return None
        with db.cursor(conn) as cur:
            # update the table_config so logging is correct
            self.c.table_config = table_config
            # TODO(jpatrin): Add join support for non-crate destinations

            # TODO(jpatrin): Disabling min and max checks for now as the query is different for crate vs. mysql
            if self.c.migration_type == orm.MigrationType.DELTA:
                if table_config.join:
                    self.log_warning('Verification is unsupported for tables in delta migrations with a join clause')
                    table_data.verification_status = 'unknown'
                    table_data.update()
                    return table_data
            elif self.c.migration_type != orm.MigrationType.FULL:
                raise shinkansen.UnrecoverableError('Migration type %r unknown' % (self.c.migration_type,))
            # TODO(jpatrin): The verifier should technically take the join clause into account so it gets the same
            # result as the queuer and exporter, but crate doesn't support joins with aggregation. As long as the
            # destination only has the records we have inserted into it the join shouldn't be needed, though.

            (where_clauses, where_values) = worker.generate_where(conn, self.c, table_config)

            sql = (
                'SELECT COUNT(*) '  # , MIN(%(chunk_col)s), MAX(%(chunk_col)s) '
                'FROM %(schema)s.%(table)s %(table_alias)s %(where)s'  # %(join)s
            ) % {
                # 'chunk_col': chunk_col,
                'schema': self.c.destination_schema,
                'table': table_config.table_name,
                'table_alias': table_config.table_alias,
                # 'join': (self.c.table_config.join % {'schema': self.c.destination_schema}
                #          if self.c.migration_type == orm.MigrationType.DELTA
                #          or self.c.chunk_migration_type == orm.ChunkMigrationType.DIRECT
                #          else ''),
                'where': (' WHERE ' + (' AND '.join(where_clauses))) if where_clauses else ''
            }
            cur.execute(sql % {'?': conn.PARAMETER_PLACEHOLDER}, where_values)
            #(num_rows, min_id, max_id) = cur.fetchone()
            (num_rows,) = cur.fetchone()
        errors = []
        if table_data.num_records != num_rows:
            errors.append('The queued number of rows (%r) and the resulting number of rows (%r) do not match' % (
                table_data.num_records, num_rows))
        #if table_data.min_id != min_id:
        #    errors.append('The queued min_id (%r) and the resulting min_id (%r) do not match' % (
        #        table_data.min_id, min_id))
        #if table_data.max_id != max_id:
        #    errors.append('The queued max_id (%r) and the resulting max_id (%r) do not match' % (
        #        table_data.max_id, max_id))
        if len(errors) > 0:
            self.log_error('Verification errors: %s', ', '.join(errors))
            table_data.verification_status = 'failed'
        else:
            self.log('Verification succeeded')
            table_data.verification_status = 'verified'
        table_data.update()
        return table_data

    # These 2 calculate methods should be refactored in a more OO manner
    def calculate_container_verification_status(self, migration):
        # Container migration types don't do direct verification of tables, the submigrations do that
        sub_verification_statuses = {}
        for submigration in migration.get_submigrations():
            sub_verification_statuses[submigration.verification_status] = (
                sub_verification_statuses.get(submigration.verification_status, 0) + 1)
        if len(sub_verification_statuses) == 1:
            return sub_verification_statuses.keys()[0]
        elif 'failed' in sub_verification_statuses:
            return 'failed'
        else:
            return 'pending'

    def calculate_verification_status(self, migration, table_verification_statuses):
        with db.shard_connection(self.c.destination_shard, read=False) as conn:
            for table_config in config.SOURCES[self.c.source_shard]['config']['tables']:
                table_data = self.check_table(table_config, conn)
                if table_data is None:
                    continue
                table_verification_statuses.setdefault(table_data.verification_status, []).append(table_data)
                if table_data.status not in ('chunks_queued', 'empty'):
                    raise Error('Something is amiss, migration status is %r while table %r has status %r' % (
                        migration.status, table_config.table_name, table_data.status))

        if len(table_verification_statuses) == 1:
            return table_verification_statuses.keys()[0]
        # If some tables are unknown but all others are something else, use the else
        elif (
            len(table_verification_statuses) == 2
            and 'unknown' in table_verification_statuses
        ):
            return [
                s for s in table_verification_statuses.keys()
                if s != 'unknown'
            ][0]
        else:
            return 'failed'

    def verify_migration(self, migration, lock):
        table_verification_statuses = {}
        if migration.type in orm.MigrationType.__CONTAINER_TYPES__:
            migration.verification_status = self.calculate_container_verification_status(migration)
        else:
            migration.verification_status = self.calculate_verification_status(migration, table_verification_statuses)

        migration.end_time = int(time.time() * 1000)
        migration.update(lock=lock)

        if migration.verification_status == 'verified':
            self.log('Migration verified verification_status=%s', migration.verification_status)
        else:
            self.log_error(
                'Migration verification failed: %r verification_status=%s',
                {
                    key: [table.table_name for table in tables]
                    for key, tables in table_verification_statuses.items()
                },
                migration.verification_status
            )

        if migration.parent_migration_id is not None:
            self.handle_parent_migration(migration)

    def queue_migration_verification(self, migration):
        chunk_config = shinkansen.worker.ChunkConfig(
            migration_id=migration.migration_id,
            partition_val=migration.partition_val,
            namespace=migration.namespace,
            source_shard=migration.source_shard,
            destination_shard=migration.destination_shard,
            source_schema=self.c.source_schema,
            destination_schema=self.c.destination_schema,
            migration_type=migration.type,
            table_config=None, columns=None, chunk_num=None, start_id=None, chunk_size=None,
        )
        queue_verification(chunk_config)

    # These 2 handle methods should be refactored in a more OO manner
    def handle_parent_autodelta(self, migration, parent_migration):
        from shinkansen.worker import queuer

        if migration.status == 'empty':
            self.log('Auto Delta migration finished with an empty delta migration parent_migration_id=%s',
                     migration.parent_migration_id)
            self.queue_migration_verification(parent_migration)
        else:
            self.log('Auto Delta migration starting another delta migration, previous migration was not empty')
            queuer.migrate_partition_shard(
                parent_migration.partition_val, parent_migration.namespace,
                parent_migration.source_shard, parent_migration.destination_shard,
                force=False, requeue=False, migration_type=orm.MigrationType.DELTA,
                parent_migration_id=parent_migration.migration_id, latest_migration=migration)

    def handle_parent_complete(self, migration, parent_migration):
        from shinkansen.worker import queuer

        if migration.type == orm.MigrationType.AUTODELTA:
            self.queue_migration_verification(parent_migration)
        else:
            self.log('Initial migration finished for complete migration, starting AUTODELTA')
            queuer.migrate_partition_shard(
                parent_migration.partition_val, parent_migration.namespace,
                parent_migration.source_shard, parent_migration.destination_shard,
                force=False, requeue=False, migration_type=orm.MigrationType.AUTODELTA,
                parent_migration_id=parent_migration.migration_id, latest_migration=migration)

    def handle_parent_migration(self, migration):
        parent_migration = orm.Migration.get(self.redis_conn, migration_id=migration.parent_migration_id)

        if parent_migration is None:
            raise shinkansen.UnrecoverableError('parent migration %r not found' % (migration.parent_migration_id,))

        if migration.status not in ('finished', 'empty'):
            self.log_warning('Submigration %r is %r', migration.migration_id, migration.status)
            self.queue_migration_verification(parent_migration)
            return

        if parent_migration.type == orm.MigrationType.AUTODELTA:
            self.handle_parent_autodelta(migration, parent_migration)
        elif parent_migration.type == orm.MigrationType.COMPLETE:
            self.handle_parent_complete(migration, parent_migration)
        else:
            raise shinkansen.UnrecoverableError('Unknown parent migration type %r' % (parent_migration.type,))

    def _run(self):
        try:
            self.__run()
        finally:
            # Don't allow the BaseChunkWorker to set the chunk's status to failed as it has already finished
            # migration at this point.
            self.chunk = None

    def __run(self):
        start = datetime.now()

        migration = orm.Migration(self.redis_conn)
        migration.migration_id = self.c.migration_id
        # TODO: Expose a record's lock via a class method so we don't have to create a dummy object above
        lock = migration._lock()
        try:
            with lock:
                migration = orm.Migration.get(self.redis_conn, migration_id=self.c.migration_id)
                if migration.verification_status in ('verified', 'failed'):
                    self.log_debug('This migration has already finished verification, not reverifying')
                    return

                migration_status = status.get_migration_status(migration_id=self.c.migration_id)
                migration.status = migration_status.computed_status
                migration.update(lock=lock)

                if migration_status.computed_status in ('finished', 'empty'):
                    self.verify_migration(migration, lock)
                else:
                    self.log_debug('Migration not finished or empty (%r), skipping verification for now',
                                   migration_status)
                    return

        except redlock.lock.RedLockError:
            msg = 'Failed to acquire lock on migration record, requeueing verification'
            self.log_debug(msg)
            raise shinkansen.worker.RetryException(msg)

        self.log('Finished verify elapsed=%s', datetime.now() - start)


if config.QUEUE_SYSTEM == 'multiprocessing':
    VERIFY_QUEUES = {}
    for _shard_config in config.DESTINATIONS.values():
        if _shard_config['config']['queue_key'] in VERIFY_QUEUES:
            continue
        VERIFY_QUEUES[_shard_config['config']['queue_key']] = multiprocessing.JoinableQueue()

    def queue_verification(chunk_config):
        VERIFY_QUEUES[
            config.DESTINATIONS[chunk_config.destination_shard]['config']['queue_key']
        ].put(chunk_config)

elif config.QUEUE_SYSTEM == 'celery':
    VERIFY_TASKS = {}
    for _shard_config in config.DESTINATIONS.values():
        if _shard_config['config']['queue_key'] in VERIFY_TASKS:
            continue
        VERIFY_TASKS[_shard_config['config']['queue_key']] = celery_app.task(
            bind=True,
            name='shinkansen.worker.verify_' + _shard_config['config']['queue_key']
        )(migration_task_wrapper(VerifyWorker))

    def queue_verification(chunk_config):
        # TODO(jpatrin): Add a unique identifier to this verification task and store this as a "key" for the lock
        # the verifier acquires. If the id doesn't match then we know a verification task has been queued after us.
        # We want the last-queued verify task to win as the countdown below is meant to allow the destination to
        # catch up (become eventually consistent).
        VERIFY_TASKS[
            config.DESTINATIONS[chunk_config.destination_shard]['config']['queue_key']
        ].apply_async([chunk_config], countdown=config.VERIFICATION_DELAY)
