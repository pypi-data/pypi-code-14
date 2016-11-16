from copy import deepcopy
from datetime import datetime
import logging
import multiprocessing

from shinkansen import config
from shinkansen import db, orm, status
from shinkansen.worker import (
    celery_app, migration_task_wrapper, verifier,
    BaseChunkWorker, Error, UnrecoverableError
)
from shinkansen.worker import exporter


log = logging.getLogger(__name__)


def generate_primary_key_sql(columns, values):
    """Generates the SQL needed to get records ordered after the values given for the columns given, in the same order
    they are used in an ORDER BY clause.
    """
    sql = '%s > %%(?)s' % (columns[0].name,)
    if len(columns) > 1:
        (sub_sql, sub_values) = generate_primary_key_sql(columns[1:], values[1:])
        return (
            '%s OR (%s = %%(?)s AND %s)' % (
                sql,
                columns[0].name,
                sub_sql,
            ),
            (values[0], values[0]) + sub_values
        )
    else:
        return (sql, tuple(values))


class PipeChunkWorker(BaseChunkWorker):
    """The PipeChunkWorker handles migration of chunks through a simple query on the source and upserts on the
    destination.

    If crate is the source and certain criteria are met[1] then the chunk is passed back to the exporter instead.

    [1] Chunk larger than MAX_CRATE_RESULT_SIZE and chunk cannot be broken up into sub-chunks by ordering with a
    primary key. This can happen due to the table not having a primary key or by the primary key including a column
    which is not usable in an ORDER BY clause. Both unindexed columns and columns which are used for partitioning
    are not usable in an ORDER BY clause.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('log', log)
        super(PipeChunkWorker, self).__init__(*args, **kwargs)

    def upsert(self, conn, records, _recursed=False):
        with db.cursor(conn) as cur:
            sql = (
                'INSERT INTO %(schema)s.%(table)s (%(columns)s) VALUES (%(placeholders)s) '
                'ON DUPLICATE KEY UPDATE %(sets)s'
            ) % {
                'schema': self.c.destination_schema,
                'table': self.c.table_config.table_name,
                'columns': ', '.join(col.name for col in self.c.export_columns),
                'placeholders': ', '.join(
                    conn.column_insert_sql(col) for col in self.c.export_columns
                ) % {'?': conn.PARAMETER_PLACEHOLDER},
                'sets': ', '.join(
                    '%s = VALUES(%s)' % (col.name, col.name)
                    for col in self.c.export_columns
                    if not col.is_primary_key
                ),
            }
            try:
                results = cur.executemany(sql, records)
            except Exception, e:
                if config.IGNORE_CONSTRAINT_FAILURES and 'foreign key constraint fails' in str(e) and not _recursed:
                    self.log('Foreign key constraint error, trying one by one')
                    for record in records:
                        try:
                            self.upsert(conn, [record], _recursed=True)
                        except Exception, e:
                            self.log('Record failed insert due to %r: %r', e, record)
                    return
                else:
                    raise
            num_rows = 0
            errors = []
            if results:
                for result in results:
                    if result['rowcount'] > -1:
                        num_rows += result['rowcount']
                    else:
                        self.log_error('Error upserting %r' % (result,))
                        errors.append(result)
            self.chunk.num_records_imported += num_rows
            self.chunk.update()
            self.log_debug('Upserted num_records=%r', num_rows)
            if errors:
                raise Error('Errors when upserting %r' % (errors,))
        conn.commit()

    def migrate(self, source_conn, dest_conn):
        # TODO: Implement option #2 as well as large numbers of records will not work with option #1 and crate.
        #       The python crate client always loads all result records into memory before returning anything
        #       (it doesn't support streaming results, like any normal DB API would), so we need to either support
        #       both of these options and switch between them at some threshold of record count or just use the second
        #       option.

        # When migrating from crate we need to either have an explicit limit or work around the implicit limit of
        # 10000 records. In order to make this work we need to do one of the following:
        #
        # 1) pre-query for the count and use that as the explicit limit (plus a fudge factor? multiplied?)
        #  * prone to errors if the number of records in the chunk would change between query time and the final
        #    SELECT. If the number of records increases enough between the COUNT and the SELECT in the result then
        #    the query could miss some of the records and not get picked up by a later autodelta as they would not
        #    have been updated.
        #  * Can mitigate by running the count then multiplying it by 2. Use that as the explicit LIMIT. Check the
        #    number of records we got vs. that limit. If we got exactly that number of records we need to try again
        #    with the limit doubled again.
        #    * This means we're re-doing all of the work but the possibility of this happening should be low enough
        #      that this only happens in extreme circumstances.
        #
        # 2) add an ORDER BY and use the ordered column to query for more records after each SELECT finishes.
        #  * adding ORDER BY slows down the query and adds load to the source database
        #  * prone to missing records which might have been inserted below any record we get on each loop
        #    i.e. assumes that the ordered field is an always increasing id field, like a mysql autoincrement id
        #  * using autodelta migrations (or a complete migration) should mean that any records potentially missed
        #    would be picked up by the delta migrations
        #  * ORDER BY and LIMIT only works if we have a unique column or primary key to use as an extra WHERE clause.
        #    Any primary key could potentially work but the problem is defining the where clause to get a part of the
        #    ordering.
        #    * This should be fixable by using ORDER BY and LIMIT with OFFSET, but this is less efficient than the extra
        #      WHERE clause as it means the server needs to scan the results to the OFFSET value each time.
        #
        # We need to implement #2 due to crate-python's inability to stream results. Very large results will not only
        # slow down the processing but are likely to cause memory errors in this module.
        #
        # XHGUTUYGJHGH crate can't sort by a partitioned column. If the primary key has a partition column then we
        # can't use the ORDER, LIMIT, WHERE pk > max option.
        # The only option in this case is to use ORDER, LIMIT, OFFSET while ordering only by the non-partition primary
        # key columns.
        #
        # What about a table where a single primary key column is also the partition column? We could potentially use
        # all indexed non-partition columns in the ORDER BY but this slows down the query.
        #
        # Maybe the right thing would just be to use COPY WHERE TO and stream the json files from the data nodes and
        # upsert them to the destination from there. That way we don't have to perform any heroics to get any data
        # out of crate. The downside, of course, is that we'll need to ssh to the data nodes to stream the files.
        # * Can use COPY table (columns...) WHERE ... TO DIRECTORY ... WITH (format='json_array') to reduce duplication
        #   of keys in the json.

        wheres = deepcopy(self.c.where_clauses) + [
            '%s >= %%(?)s' % (self.c.table_config.chunk_col,),
            '%s < %%(?)s' % (self.c.table_config.chunk_col,),
        ]
        base_values = deepcopy(self.c.where_values) + [
            self.c.start_id,
            self.c.start_id + self.c.chunk_size,
        ]

        if self.c.migration_type == orm.MigrationType.DELTA and self.c.table_config.join:
            if self.c.source_type == 'crate':
                self.log('Chunk cannot be piped, migration type is delta, table has a join, and source is crate. '
                         'Chunk will be exported and streamed instead.')
                self.chunk.status = 'queued'
                self.chunk.update()
                exporter.queue_export_chunk(self.c)
                return False
            join = self.c.table_config.join % {'schema': self.c.source_schema}
        else:
            join = ''

        base_sql = (
            'FROM %(schema)s.%(table)s %(table_alias)s %(join)s '
            'WHERE %(where_clauses)s'
        ) % {
            'schema': self.c.source_schema,
            'table': self.c.table_config.table_name,
            'table_alias': self.c.table_config.table_alias,
            'join': join,
            'where_clauses': ' AND '.join(wheres)
        }

        # crate has an implicit limit of 10000, we query for the count here to make sure we get all
        # of the records
        if self.c.source_type == 'crate':
            self.log('Querying for chunk size')
            sql = 'SELECT COUNT(*) %s' % (base_sql,)
            with db.cursor(source_conn) as source_cur:
                source_cur.execute(sql % {'?': source_conn.PARAMETER_PLACEHOLDER}, base_values)
                (count,) = source_cur.fetchone()

            if not count:
                self.log('No data found for chunk')
                return True

            use_order = count > config.MAX_CRATE_RESULT_SIZE

            if use_order:
                (
                    primary_key_indexes,
                    primary_key_columns,
                ) = zip(*[
                    (
                        i,
                        col,
                    )
                    for (i, col) in enumerate(self.c.export_columns)
                    if col.is_primary_key
                ])
                use_offset = False
                if not primary_key_columns:
                    self.log_warning('Table has no primary key columns')
                    use_offset = True
                else:
                    unorderable_columns = [
                        col.lower() for col in
                        source_conn.get_unorderable_columns(
                            self.c.source_schema,
                            self.c.table_config.table_name
                        )
                    ]
                    if any(pkc.name.lower() in unorderable_columns for pkc in primary_key_columns):
                        self.log_warning('Table has primary key columns that cannot be used for sorting')
                        use_offset = True

                if use_offset:
                    self.log('Chunk cannot be piped, it must be exported and streamed')
                    self.chunk.status = 'queued'
                    self.chunk.update()
                    exporter.queue_export_chunk(self.c)
                    return False

                #     self.log_warning(
                #         'Falling back to full ordering and LIMIT OFFSET querying. Depending on the cardinality of the '
                #         'fields this may be very expensive or miss records depending on whether the sort order is '
                #         'deterministic.'
                #     )
                #     (
                #         key_indexes,
                #         key_columns
                #     ) = zip(*[
                #         (
                #             i,
                #             col,
                #         )
                #         for (i, col) in enumerate(self.c.export_columns)
                #         if col.name.lower() not in unorderable_columns
                #     ])

                else:
                    self.log(
                        'Chunk size (%u) is larger than the configured MAX_CRATE_RESULT_SIZE (%u). '
                        'This chunk will be broken up into multiple ordered queries.' % (
                            count,
                            config.MAX_CRATE_RESULT_SIZE,
                        )
                    )
                    key_indexes = primary_key_indexes
                    key_columns = primary_key_columns

                # if not key_columns:
                #     raise UnrecoverableError(
                #         'No sortable columns found, cannot migrate this chunk as it is larger '
                #         'than MAX_CRATE_RESULT_SIZE'
                #     )

                limit = config.MAX_CRATE_RESULT_SIZE
                order_sql = 'ORDER BY %s LIMIT %u' % (
                    ', '.join(col.name for col in key_columns),
                    limit
                )
            else:
                limit = count
        else:
            use_order = False

        self.chunk.num_records_exported = 0
        self.chunk.update()

        key_max_values = []

        while True:
            # TODO: Refactor?
            if use_order:
                if use_offset:
                    raise UnrecoverableError('Implement ORDER LIMIT OFFSET?')
                else:
                    if key_max_values:
                        # WHERE c1 > mv1 OR c1 == mv1 AND (c2 > mv2 OR c2 == mv2 AND c3 > mv3)
                        (
                            primary_key_sql,
                            primary_key_values,
                        ) = generate_primary_key_sql(key_columns, key_max_values)
                        loop_values = list(base_values) + list(primary_key_values)
                        loop_base_sql = '%s AND %s %s' % (
                            base_sql,
                            primary_key_sql,
                            order_sql,
                        )
                    else:
                        loop_base_sql = '%s %s' % (
                            base_sql,
                            order_sql,
                        )
                        loop_values = base_values
            elif self.c.source_type == 'crate':
                limit *= 2
                loop_base_sql = '%s LIMIT %u' % (base_sql, limit)
                loop_values = base_values
            else:
                loop_base_sql = base_sql
                loop_values = base_values

            sql = (
                'SELECT %s %s'
            ) % (
                ', '.join(
                    source_conn.column_query_sql(col)
                    for col in self.c.export_columns
                ),
                loop_base_sql,
            )
            if not use_order:
                self.chunk.num_records_exported = 0
                self.chunk.update()

            with db.cursor(source_conn) as source_cur:
                source_cur.execute(sql % {'?': source_conn.PARAMETER_PLACEHOLDER}, loop_values)
                num_recs = 0
                while True:
                    records = source_cur.fetchmany(config.PIPE_BULK_INSERT_SIZE)
                    if not records:
                        break
                    self.chunk.num_records_exported += len(records)
                    self.chunk.update()
                    num_recs += len(records)
                    if use_order and not use_offset:
                        new_key_max_values = []
                        for col_idx_idx in xrange(len(key_indexes)):
                            max_val = max(r[key_indexes[col_idx_idx]] for r in records)
                            if key_max_values:
                                max_val = max(max_val, key_max_values[col_idx_idx])
                            new_key_max_values.append(max_val)
                        key_max_values = new_key_max_values
                    self.log_debug('Got records from source num_records=%s', len(records))
                    self.upsert(dest_conn, records)

            if self.c.source_type == 'crate':
                if use_order:
                    if num_recs < limit:
                        self.log('Chunk finished num_recs=%u limit=%u', num_recs, limit)
                        break
                    else:
                        self.log(
                            'Chunk has more records key_max_values=%r num_recs=%u limit=%u',
                            key_max_values, num_recs, limit
                        )
                # if we got as many records as the limit set above it is likely there were more than that to get
                # so we need to loop and do it over with a higher limit
                elif self.chunk.num_records_exported < limit:
                    break
                else:
                    self.log(
                        'The number of records has grown more than double, retrying with double the limit limit=%u',
                        limit
                    )
            else:
                break
        return True

    def _run(self):
        start = datetime.now()
        self.log('Pipe worker starting')

        self.chunk.status = 'migrating'
        self.chunk.num_records_exported = 0
        self.chunk.num_records_imported = 0
        self.chunk.update()

        with db.shard_connection(self.c.source_shard, read=True) as source_conn:
            with db.shard_connection(self.c.destination_shard, read=False) as dest_conn:
                update_status = self.migrate(source_conn, dest_conn)

        if update_status:
            self.chunk.import_elapsed_ms = int((datetime.now() - start).total_seconds() * 1000)
            self.chunk.status = 'imported'
            self.chunk.update()

            (migration_status, _, _, _, _) = status.get_migration_status(migration_id=self.c.migration_id)
            migration = orm.Migration.get(self.redis_conn, migration_id=self.c.migration_id)
            migration.status = migration_status
            migration.update()

        if config.ENABLE_VERIFIER:
            verifier.queue_verification(self.c)

        self.log('Pipe worker finished elapsed=%s', datetime.now() - start)


if config.QUEUE_SYSTEM == 'multiprocessing':
    PIPE_QUEUES = {}
    for _shard_config in config.SOURCES.values():
        if _shard_config['config']['queue_key'] in PIPE_QUEUES:
            continue
        PIPE_QUEUES[_shard_config['config']['queue_key']] = multiprocessing.JoinableQueue()

    def queue_pipe_chunk(chunk_config):
        PIPE_QUEUES[
            config.SOURCES[chunk_config.source_shard]['config']['queue_key']
        ].put(chunk_config)

elif config.QUEUE_SYSTEM == 'celery':
    PIPE_TASKS = {}
    for _shard_config in config.SOURCES.values():
        if _shard_config['config']['queue_key'] in PIPE_TASKS:
            continue
        PIPE_TASKS[_shard_config['config']['queue_key']] = celery_app.task(
            bind=True,
            name='shinkansen.worker.pipe_' + _shard_config['config']['queue_key']
        )(migration_task_wrapper(PipeChunkWorker))

    def queue_pipe_chunk(chunk_config):
        PIPE_TASKS[
            config.SOURCES[chunk_config.source_shard]['config']['queue_key']
        ].delay(chunk_config)
