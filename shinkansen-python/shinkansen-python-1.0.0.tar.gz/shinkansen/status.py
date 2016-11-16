import collections
import logging

import shinkansen
from shinkansen import orm
import shinkansen.db


log = logging.getLogger(__name__)


MigrationStatus = collections.namedtuple(
    'MigrationStatus',
    [
        'computed_status',
        'computed_verification_status',
        'chunk_statuses',
        'table_statuses',
        'table_verification_statuses',
    ]
)


def get_autodelta_migration_status(migration):
    submigration = migration.get_latest_submigration()
    if submigration is None:
        status = 'unknown'
    elif submigration.status == 'empty':
        status = 'finished'
    else:
        status = 'in_progress'
    return MigrationStatus(status, '', {}, {}, {})


def get_complete_migration_status(migration):
    submigration = migration.get_latest_submigration()
    if submigration.type == orm.MigrationType.AUTODELTA:
        if submigration.status == 'queued':
            status = 'in_progress'
        else:
            status = submigration.status
    else:
        if submigration.status in ('finished', 'empty'):
            status = 'in_progress'
        else:
            status = submigration.status

    return MigrationStatus(status, '', {}, {}, {})


def get_migration_status(source=None, destination=None, partition_val=None, migration_id=None):
    if partition_val is None and migration_id is None:
        raise shinkansen.UnrecoverableError('partition_val or migration_id must be provided')
    if source is None and destination is not None or source is not None and destination is None:
        raise shinkansen.UnrecoverableError('source and destination must either both be provided or both be None')
    clauses = {}
    if partition_val is not None:
        clauses['partition_val'] = partition_val
    if source is not None:
        clauses['source_shard'] = source
    if destination is not None:
        clauses['destination_shard'] = destination
    if migration_id is not None:
        if clauses:
            raise shinkansen.UnrecoverableError('When migration_id is specified it must be the only argument')
        clauses['migration_id'] = migration_id

    table_statuses = {}
    table_verification_statuses = {}
    chunk_statuses = {}
    with shinkansen.db.redis_conn() as redis:
        if migration_id is not None:
            migration = orm.Migration.get(redis, migration_id=migration_id)
            if migration.type == orm.MigrationType.AUTODELTA:
                return get_autodelta_migration_status(migration)
            elif migration.type == orm.MigrationType.COMPLETE:
                return get_complete_migration_status(migration)

        for table_rec in orm.Table.get_by_index(redis, **clauses):
            table_statuses.setdefault(table_rec.status, 0)
            table_statuses[table_rec.status] += 1

            table_verification_statuses.setdefault(table_rec.verification_status, 0)
            table_verification_statuses[table_rec.verification_status] += 1

        for chunk_rec in orm.Chunk.get_by_index(redis, **clauses):
            chunk_statuses.setdefault(chunk_rec.status, 0)
            chunk_statuses[chunk_rec.status] += 1

    if len(table_statuses) == 0 and len(chunk_statuses) == 0:
        status = 'not_started'
    elif 'failed' in table_statuses or 'failed' in chunk_statuses:
        status = 'failed'
    elif len(chunk_statuses) == 0 and len(table_statuses) == 1 and 'empty' in table_statuses:
        status = 'empty'
    elif (
        (len(table_statuses) == 1 and 'queued' in table_statuses)
        or (len(chunk_statuses) == 1 and 'queued' in chunk_statuses)
    ):
        status = 'queued'
    elif (((len(chunk_statuses) == 1 or (len(chunk_statuses) == 2 and 'empty' in chunk_statuses))
           and 'imported' in chunk_statuses)
          and ((len(table_statuses) == 1 or (len(table_statuses) == 2 and 'empty' in table_statuses))
               and 'chunks_queued' in table_statuses)):
        status = 'finished'
    else:
        status = 'in_progress'

    if len(table_verification_statuses) == 1:
        verification_status = table_verification_statuses.keys()[0]
    # If some tables are unknown but all others are something else, use the else
    elif (
        len(table_verification_statuses) == 2
        and 'unknown' in table_verification_statuses
    ):
        verification_status = [
            s for s in table_verification_statuses.keys()
            if s != 'unknown'
        ][0]
    elif 'failed' in table_verification_statuses:
        verification_status = 'failed'
    else:
        verification_status = 'pending'

    return MigrationStatus(
        status, verification_status,
        chunk_statuses, table_statuses, table_verification_statuses,
    )


def get_table_migration_status(source=None, destination=None, partition_val=None, migration_id=None):
    if partition_val is None and migration_id is None:
        raise shinkansen.UnrecoverableError('partition_val or migration_id must be provided')
    if source is None and destination is not None or source is not None and destination is None:
        raise shinkansen.UnrecoverableError('source and destination must either both be provided or both be None')

    clauses = {}
    if partition_val is not None:
        clauses['partition_val'] = partition_val
    if source is not None:
        clauses['source_shard'] = source
    if destination is not None:
        clauses['destination_shard'] = destination
    if migration_id is not None:
        clauses['migration_id'] = migration_id

    tables = {}
    with shinkansen.db.redis_conn() as redis:
        for table_rec in orm.Table.get_by_index(redis, **clauses):
            if table_rec.table_name in tables:
                log.warn(
                    'Multiple entries for table, last one will win '
                    'partition_val=%s table_name=%s source=%s destination=%s',
                    partition_val, table_rec.table_name, source, destination
                )
            table = {
                'partition_val': partition_val,
                'num_records_exported': 0,
                'num_records_converted': 0,
                'num_records_imported': 0,
                'num_chunks': table_rec.num_chunks,
                'export_elapsed_ms': 0,
                'convert_elapsed_ms': 0,
                'import_elapsed_ms': 0,
                'chunk_size': table_rec.chunk_size,
                'min_id': table_rec.min_id,
                'max_id': table_rec.max_id,
                'num_records_total': table_rec.num_records,
                'status': table_rec.status,
                'verification_status': table_rec.verification_status,
                'queued_time': table_rec.queued_time,
                'start_time': table_rec.start_time,
                'end_time': table_rec.end_time,
            }
            for key in table:
                if table[key] is None:
                    table[key] = 0
            tables[table_rec.table_name] = table

        for chunk_rec in orm.Chunk.get_by_index(redis, **clauses):
            if chunk_rec.table_name not in tables:
                log.warn(
                    'Table has chunks but no entry, potential data corruption '
                    'partition_val=%s table_name=%s source=%s destination=%s',
                    partition_val, chunk_rec.table_name, source, destination
                )
                tables[chunk_rec.table_name] = {
                    'partition_val': partition_val,
                    'num_records_exported': 0,
                    'num_records_converted': 0,
                    'num_records_imported': 0,
                    'num_chunks': 0,
                    'export_elapsed_ms': 0,
                    'convert_elapsed_ms': 0,
                    'import_elapsed_ms': 0,
                }
            table = tables[chunk_rec.table_name]
            for key in [
                'num_records_exported',
                'num_records_converted',
                'num_records_imported',
                'export_elapsed_ms',
                'convert_elapsed_ms',
                'import_elapsed_ms',
            ]:
                val = getattr(chunk_rec, key)
                if val is not None:
                    table[key] += int(val)
                else:
                    table.setdefault(key, 0)

            table.setdefault('num_chunks_' + chunk_rec.status, 0)
            table['num_chunks_' + chunk_rec.status] += 1

    return tables
