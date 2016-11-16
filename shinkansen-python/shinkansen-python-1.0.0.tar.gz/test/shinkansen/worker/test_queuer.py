from collections import OrderedDict
import contextlib

import mox

from shinkansen import config, data, db, orm, worker
from shinkansen.worker import queuer


@contextlib.contextmanager
def context(ret):
    yield ret


class TestQueuerTopLevelAPI(mox.MoxTestBase):
    def setUp(self):
        super(TestQueuerTopLevelAPI, self).setUp()

        # Keep these in order so the tests, which rely on ordering, don't fail
        config.SHARD_SUFFIXES = OrderedDict([
            ('daily', ''),
            ('weekly', '_w'),
            ('monthly', '_m'),
        ])
        config.MYSQL_SHARDS = {
            'shn': {
                'tables': [
                    data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None),
                    data.TableConfig('TableB', 'filter_col_b', 'chunk_col_b', None),
                ],
                'default_schema_name': 'mysql',
            },
            'shn_w': {
                'tables': [
                    data.TableConfig('WTableA', 'w_filter_col_a', 'w_chunk_col_a', None),
                    data.TableConfig('WTableB', 'w_filter_col_b', 'w_chunk_col_b', None),
                ],
                'default_schema_name': 'mysql_w',
            },
            'shn_m': {
                'tables': [
                    data.TableConfig('MTableA', 'm_filter_col_a', 'm_chunk_col_a', None),
                    data.TableConfig('MTableB', 'm_filter_col_b', 'm_chunk_col_b', None),
                ],
                'default_schema_name': 'mysql_m',
            },
        }
        config.CRATE_SHARDS = {
            'crate': {
                'default_schema_name': 'crate',
            },
            'crate_w': {
                'default_schema_name': 'crate_w',
            },
            'crate_m': {
                'default_schema_name': 'crate_m',
            },
        }
        config.SOURCES = {
            'shn': {'type': 'mysql'},
            'shn_w': {'type': 'mysql'},
            'shn_m': {'type': 'mysql'},
        }
        config.DESTINATIONS = {
            'crate': {'type': 'crate'},
            'crate_w': {'type': 'crate'},
            'crate_m': {'type': 'crate'},
        }
        for key, values in config.SOURCES.items():
            values['config'] = config.MYSQL_SHARDS[key]
        for key, values in config.DESTINATIONS.items():
            values['config'] = config.CRATE_SHARDS[key]

        self.mox.StubOutWithMock(queuer, 'queue_migrate_table')
        self.mox.StubOutWithMock(db, 'crate_conn')
        self.mox.StubOutWithMock(orm, 'Table')
        self.mox.StubOutWithMock(orm.Table, 'get')
        self.mox.StubOutWithMock(orm.Table, 'insert')
        self.mox.StubOutWithMock(db, 'redis_conn')
        self.mox.StubOutWithMock(db, 'shard_connection')
        self.mox.StubOutWithMock(orm, 'Migration')

    def expected_configs(self, configs):
        new_conn = True
        for chunk_config in configs:
            if new_conn:
                redis_conn = self.mox.CreateMockAnything()
                db.redis_conn().AndReturn(redis_conn)
                redis_conn.__enter__().AndReturn(redis_conn)

                orm.Migration.get_latest(
                    redis_conn,
                    source_shard=chunk_config.source_shard, destination_shard=chunk_config.destination_shard,
                    partition_val=chunk_config.partition_val
                ).AndReturn(None)

                migration = self.mox.CreateMockAnything()
                migration._redis = redis_conn
                orm.Migration(redis_conn).AndReturn(migration)

                conn = self.mox.CreateMockAnything()
                db.shard_connection(chunk_config.source_shard, read=True).AndReturn(context(conn))
                conn.get_current_timestamp().AndReturn(123)

                migration.insert()
            else:
                redis_conn.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
            new_conn = not new_conn
            tt = self.mox.CreateMockAnything()
            orm.Table(redis_conn).AndReturn(tt)
            tt.insert()
            queuer.queue_migrate_table(chunk_config)

    def test_migrate_partition(self):
        partition_val = 13
        source_shard = 'shn'
        destination_shard = 'crate'
        namespace = ''
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None), None, partition_val,
                               namespace, source_shard, destination_shard, None, None, None,
                               'mysql', 'crate'),

            worker.ChunkConfig('mid', data.TableConfig('TableB', 'filter_col_b', 'chunk_col_b', None), None, partition_val,
                               namespace, source_shard, destination_shard, None, None, None,
                               'mysql', 'crate'),

            worker.ChunkConfig('mid', data.TableConfig('WTableA', 'w_filter_col_a', 'w_chunk_col_a', None), None,
                               partition_val,
                               namespace, source_shard + '_w', destination_shard + '_w', None, None, None,
                               'mysql_w', 'crate_w'),

            worker.ChunkConfig('mid', data.TableConfig('WTableB', 'w_filter_col_b', 'w_chunk_col_b', None), None,
                               partition_val,
                               namespace, source_shard + '_w', destination_shard + '_w', None, None, None,
                               'mysql_w', 'crate_w'),

            worker.ChunkConfig('mid', data.TableConfig('MTableA', 'm_filter_col_a', 'm_chunk_col_a', None), None,
                               partition_val,
                               namespace, source_shard + '_m', destination_shard + '_m', None, None, None,
                               'mysql_m', 'crate_m'),

            worker.ChunkConfig('mid', data.TableConfig('MTableB', 'm_filter_col_b', 'm_chunk_col_b', None), None,
                               partition_val,
                               namespace, source_shard + '_m', destination_shard + '_m', None, None, None,
                               'mysql_m', 'crate_m'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition(partition_val, namespace, source_shard, destination_shard)

    def test_migrate_partition_namespace(self):
        partition_val = 13
        source_shard = 'shn'
        destination_shard = 'crate'
        namespace = 'ns'
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None), None, partition_val,
                               'ns', source_shard, destination_shard, None, None, None,
                               'ns', 'ns'),

            worker.ChunkConfig('mid', data.TableConfig('TableB', 'filter_col_b', 'chunk_col_b', None), None, partition_val,
                               'ns', source_shard, destination_shard, None, None, None,
                               'ns', 'ns'),

            worker.ChunkConfig('mid', data.TableConfig('WTableA', 'w_filter_col_a', 'w_chunk_col_a', None), None,
                               partition_val,
                               'ns_w', source_shard + '_w', destination_shard + '_w', None, None, None,
                               'ns_w', 'ns_w'),

            worker.ChunkConfig('mid', data.TableConfig('WTableB', 'w_filter_col_b', 'w_chunk_col_b', None), None,
                               partition_val,
                               'ns_w', source_shard + '_w', destination_shard + '_w', None, None, None,
                               'ns_w', 'ns_w'),

            worker.ChunkConfig('mid', data.TableConfig('MTableA', 'm_filter_col_a', 'm_chunk_col_a', None), None,
                               partition_val,
                               'ns_m', source_shard + '_m', destination_shard + '_m', None, None, None,
                               'ns_m', 'ns_m'),

            worker.ChunkConfig('mid', data.TableConfig('MTableB', 'm_filter_col_b', 'm_chunk_col_b', None), None,
                               partition_val,
                               'ns_m', source_shard + '_m', destination_shard + '_m', None, None, None,
                               'ns_m', 'ns_m'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition(partition_val, namespace, source_shard, destination_shard)

    def test_migrate_partition_shard(self):
        partition_val = 13
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None), None, partition_val,
                               '', 'shn', 'crate', None, None, None,
                               'mysql', 'crate'),

            worker.ChunkConfig('mid', data.TableConfig('TableB', 'filter_col_b', 'chunk_col_b', None), None, partition_val,
                               '', 'shn', 'crate', None, None, None,
                               'mysql', 'crate'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition_shard(partition_val, '', 'shn', 'crate')

    def test_migrate_partition_shard_w(self):
        partition_val = 13
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('WTableA', 'w_filter_col_a', 'w_chunk_col_a', None), None,
                               partition_val,
                               '', 'shn_w', 'crate_w', None, None, None,
                               'mysql_w', 'crate_w'),

            worker.ChunkConfig('mid', data.TableConfig('WTableB', 'w_filter_col_b', 'w_chunk_col_b', None), None,
                               partition_val,
                               '', 'shn_w', 'crate_w', None, None, None,
                               'mysql_w', 'crate_w'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition_shard(partition_val, '', 'shn_w', 'crate_w')

    def test_migrate_partition_shard_m(self):
        partition_val = 13
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('MTableA', 'm_filter_col_a', 'm_chunk_col_a', None), None,
                               partition_val,
                               '', 'shn_m', 'crate_m', None, None, None,
                               'mysql_m', 'crate_m'),

            worker.ChunkConfig('mid', data.TableConfig('MTableB', 'm_filter_col_b', 'm_chunk_col_b', None), None,
                               partition_val,
                               '', 'shn_m', 'crate_m', None, None, None,
                               'mysql_m', 'crate_m'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition_shard(partition_val, '', 'shn_m', 'crate_m')

    def test_migrate_partition_shard_namespace(self):
        partition_val = 13
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None), None, partition_val,
                               'ns', 'shn', 'crate', None, None, None,
                               'ns', 'ns'),

            worker.ChunkConfig('mid', data.TableConfig('TableB', 'filter_col_b', 'chunk_col_b', None), None, partition_val,
                               'ns', 'shn', 'crate', None, None, None,
                               'ns', 'ns'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition_shard(partition_val, 'ns', 'shn', 'crate')

    def test_migrate_partition_shard_w_namespace(self):
        partition_val = 13
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('WTableA', 'w_filter_col_a', 'w_chunk_col_a', None), None,
                               partition_val,
                               'ns', 'shn_w', 'crate_w', None, None, None,
                               'ns', 'ns'),

            worker.ChunkConfig('mid', data.TableConfig('WTableB', 'w_filter_col_b', 'w_chunk_col_b', None), None,
                               partition_val,
                               'ns', 'shn_w', 'crate_w', None, None, None,
                               'ns', 'ns'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition_shard(partition_val, 'ns', 'shn_w', 'crate_w')

    def test_migrate_partition_shard_m_namespace(self):
        partition_val = 13
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('MTableA', 'm_filter_col_a', 'm_chunk_col_a', None), None,
                               partition_val,
                               'ns', 'shn_m', 'crate_m', None, None, None,
                               'ns', 'ns'),

            worker.ChunkConfig('mid', data.TableConfig('MTableB', 'm_filter_col_b', 'm_chunk_col_b', None), None,
                               partition_val,
                               'ns', 'shn_m', 'crate_m', None, None, None,
                               'ns', 'ns'),
        ]
        self.expected_configs(configs)

        self.mox.ReplayAll()
        queuer.migrate_partition_shard(partition_val, 'ns', 'shn_m', 'crate_m')

    def test_migrate_partition_skips_missing_sources(self):
        del config.SOURCES['shn_w']

        partition_val = 13
        source_shard = 'shn'
        destination_shard = 'crate'
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None), None, partition_val,
                               '', source_shard, destination_shard, None, None, None,
                               'mysql', 'crate'),

            worker.ChunkConfig('mid', data.TableConfig('TableB', 'filter_col_b', 'chunk_col_b', None), None, partition_val,
                               '', source_shard, destination_shard, None, None, None,
                               'mysql', 'crate'),

            worker.ChunkConfig('mid', data.TableConfig('MTableA', 'm_filter_col_a', 'm_chunk_col_a', None), None,
                               partition_val,
                               '', source_shard + '_m', destination_shard + '_m', None, None, None,
                               'mysql_m', 'crate_m'),

            worker.ChunkConfig('mid', data.TableConfig('MTableB', 'm_filter_col_b', 'm_chunk_col_b', None), None,
                               partition_val,
                               '', source_shard + '_m', destination_shard + '_m', None, None, None,
                               'mysql_m', 'crate_m'),
        ]
        self.expected_configs(configs)

        namespace = ''

        self.mox.ReplayAll()
        queuer.migrate_partition(partition_val, namespace, source_shard, destination_shard)

    def test_migrate_partition_skips_missing_destinations(self):
        del config.DESTINATIONS['crate_m']

        partition_val = 13
        source_shard = 'shn'
        destination_shard = 'crate'
        configs = [
            worker.ChunkConfig('mid', data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None), None, partition_val,
                               '', source_shard, destination_shard, None, None, None,
                               'mysql', 'crate'),

            worker.ChunkConfig('mid', data.TableConfig('TableB', 'filter_col_b', 'chunk_col_b', None), None, partition_val,
                               '', source_shard, destination_shard, None, None, None,
                               'mysql', 'crate'),

            worker.ChunkConfig('mid', data.TableConfig('WTableA', 'w_filter_col_a', 'w_chunk_col_a', None), None,
                               partition_val,
                               '', source_shard + '_w', destination_shard + '_w', None, None, None,
                               'mysql_w', 'crate_w'),

            worker.ChunkConfig('mid', data.TableConfig('WTableB', 'w_filter_col_b', 'w_chunk_col_b', None), None,
                               partition_val,
                               '', source_shard + '_w', destination_shard + '_w', None, None, None,
                               'mysql_w', 'crate_w'),
        ]
        self.expected_configs(configs)

        namespace = ''

        self.mox.ReplayAll()
        queuer.migrate_partition(partition_val, namespace, source_shard, destination_shard)


class TestQueueChunksWorker(mox.MoxTestBase):
    def setUp(self):
        super(TestQueueChunksWorker, self).setUp()
        config.SOURCES = {
            'src': {'type': 'mysql', 'config': {}},
        }
        config.DESTINATIONS = {
            'dst': {'type': 'crate', 'config': {}},
        }

        self.config = worker.ChunkConfig(
            migration_id='mid',
            table_config=data.TableConfig('anomaly', 'tc', 'cc', None, ignore_columns=['information']),
            columns=[],
            partition_val=43,
            namespace='ns',
            source_shard='src',
            destination_shard='dst',
            chunk_num=None,
            start_id=0,
            chunk_size=1
        )
        self.redis = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(worker.orm.Migration, 'get')
        self.migration = self.mox.CreateMockAnything()
        worker.orm.Migration.get(self.redis, migration_id='mid').AndReturn(self.migration)
        self.mox.StubOutWithMock(worker.orm.Table, 'get')
        self.tt = self.mox.CreateMockAnything()
        worker.orm.Table.get(
            self.redis,
            migration_id='mid',
            partition_val=43, table_name='anomaly',
            namespace='ns',
            source_shard='src', destination_shard='dst'
        ).AndReturn(self.tt)

    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def test_get_column_metadata(self):
        self.mox.StubOutWithMock(queuer.db, 'cursor')
        cur = self.mox.CreateMockAnything()
        queuer.db.cursor(None, dictionary=True).AndReturn(self.context(cur))
        cur.execute(mox.IgnoreArg())
        cur.fetchall().AndReturn([
            {'Field': 'f1', 'Key': 'PRI', 'Type': 'int(6)'},
            {'Field': 'F2', 'Key': 'IDX', 'Type': 'int(6)'},
            {'Field': 'F3', 'Key': 'IDX', 'Type': 'timestamp'},
            {'Field': 'Information', 'Key': '', 'Type': 'float(6)'},
        ])

        self.mox.StubOutWithMock(queuer.db, 'shard_connection')
        conn = self.mox.CreateMockAnything()
        queuer.db.shard_connection('dst', read=True).AndReturn(self.context(conn))
        conn.get_table_primary_key_columns('ns', 'anomaly').AndReturn(['f1', 'f3'])

        self.mox.ReplayAll()
        self.config.migration_type = orm.MigrationType.DELTA
        worker = queuer.QueueChunksWorkerMysql(self.config, self.redis)
        worker.get_column_metadata(None)
        columns = [
            db.Column(
                'f1',
                db.ColumnType.INT,
                True,
                ignore=False,
                source_alias=''
            ),
            db.Column(
                'F2',
                db.ColumnType.INT,
                False,
                ignore=False,
                source_alias=''
            ),
            db.Column(
                'F3',
                db.ColumnType.TIMESTAMP,
                True,
                ignore=False,
                source_alias=''
            ),
            db.Column(
                'Information',
                db.ColumnType.FLOAT,
                False,
                ignore=True,
                source_alias=''
            ),
        ]
        self.assertEqual(worker.c.columns, columns)
        self.assertEqual(worker.column_map, {col.lname: col for col in columns})

    def test_get_column_metadata_delta_column_mismatch(self):
        self.mox.StubOutWithMock(queuer.db, 'cursor')
        cur = self.mox.CreateMockAnything()
        queuer.db.cursor(None, dictionary=True).AndReturn(self.context(cur))
        cur.execute(mox.IgnoreArg())
        cur.fetchall().AndReturn([
            {'Field': 'f1', 'Key': 'PRI', 'Type': 'int(6)'},
            {'Field': 'F2', 'Key': 'IDX', 'Type': 'int(6)'},
            {'Field': 'F3', 'Key': 'IDX', 'Type': 'timestamp'},
            {'Field': 'Information', 'Key': '', 'Type': 'float(6)'},
        ])

        self.mox.StubOutWithMock(queuer.db, 'shard_connection')
        conn = self.mox.CreateMockAnything()
        queuer.db.shard_connection('dst', read=True).AndReturn(self.context(conn))
        conn.get_table_primary_key_columns('ns', 'anomaly').AndReturn(['f1', 'z', 'f3'])

        self.mox.ReplayAll()
        self.config.migration_type = orm.MigrationType.DELTA
        worker = queuer.QueueChunksWorkerMysql(self.config, self.redis)
        with self.assertRaises(queuer.UnrecoverableError):
            worker.get_column_metadata(None)

    def test_queue_chunks_full(self):
        self.mox.StubOutWithMock(queuer.orm, 'Chunk')
        self.mox.StubOutWithMock(queuer.exporter, 'queue_export_chunk')

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=0, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 0, 0, 34, 'ns', 'ns', 'full', None))

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=1, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 1, 34, 34, 'ns', 'ns', 'full', None))

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=2, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 2, 68, 34, 'ns', 'ns', 'full', None))

        self.mox.ReplayAll()
        config.CHUNK_SIZE = 30
        self.config.migration_type = orm.MigrationType.FULL
        worker = queuer.QueueChunksWorker(self.config, self.redis)
        worker.min_id = 0
        worker.max_id = 100
        worker.num_rows = 80
        worker.queue_chunks()
        self.assertEqual(worker.c.chunk_size, 34)
        self.assertEqual(worker.num_chunks, 3)

    def test_queue_chunks_full_skips_existing_chunks(self):
        self.mox.StubOutWithMock(queuer.orm, 'Chunk')
        self.mox.StubOutWithMock(queuer.exporter, 'queue_export_chunk')
        done_ttc = self.mox.CreateMockAnything()
        done_ttc.status = 'imported'

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=0, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([done_ttc])

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=1, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 1, 34, 34, 'ns', 'ns', 'full', None))

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=2, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 2, 68, 34, 'ns', 'ns', 'full', None))

        self.mox.ReplayAll()
        config.CHUNK_SIZE = 30
        self.config.migration_type = orm.MigrationType.FULL
        self.config.force = False
        self.config.latest_migration_id = None
        worker = queuer.QueueChunksWorker(self.config, self.redis)
        worker.min_id = 0
        worker.max_id = 100
        worker.num_rows = 80
        worker.queue_chunks()
        self.assertEqual(worker.c.chunk_size, 34)
        self.assertEqual(worker.num_chunks, 3)

    def test_queue_chunks_full_force_existing_chunks(self):
        self.mox.StubOutWithMock(queuer.orm, 'Chunk')
        self.mox.StubOutWithMock(queuer.exporter, 'queue_export_chunk')
        done_ttc = self.mox.CreateMockAnything()
        done_ttc.status = 'imported'
        done_ttc2 = self.mox.CreateMockAnything()
        done_ttc2.status = 'empty'

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=0, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([done_ttc])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 0, 0, 34, 'ns', 'ns', 'full', None))

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=1, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn(['partition_val', 'unknown'])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 1, 34, 34, 'ns', 'ns', 'full', None))

        orm.Chunk.get_by_index(
            self.redis,
            chunk_num=2, destination_shard='dst', namespace='ns', source_shard='src',
            table_name='anomaly', partition_val=43
        ).AndReturn([done_ttc2])
        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.exporter.queue_export_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 2, 68, 34, 'ns', 'ns', 'full', None))

        self.mox.ReplayAll()
        config.CHUNK_SIZE = 30
        self.config.migration_type = orm.MigrationType.FULL
        self.config.force = True
        self.config.latest_migration_id = None
        worker = queuer.QueueChunksWorker(self.config, self.redis)
        worker.min_id = 0
        worker.max_id = 100
        worker.num_rows = 80
        worker.queue_chunks()
        self.assertEqual(worker.c.chunk_size, 34)
        self.assertEqual(worker.num_chunks, 3)

    def test_queue_chunks_delta(self):
        self.mox.StubOutWithMock(queuer.orm, 'Chunk')
        self.mox.StubOutWithMock(queuer.pipe, 'queue_pipe_chunk')

        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.pipe.queue_pipe_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 0, 0, 34, 'ns', 'ns', 'delta', None))

        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.pipe.queue_pipe_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 1, 34, 34, 'ns', 'ns', 'delta', None))

        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()
        queuer.pipe.queue_pipe_chunk(
            queuer.ChunkConfig(
                'mid', data.TableConfig('anomaly', 'tc', 'cc', None, '', '', ignore_columns=['information']),
                [], 43, 'ns', 'src', 'dst', 2, 68, 34, 'ns', 'ns', 'delta', None))

        self.mox.ReplayAll()
        config.CHUNK_SIZE = 30
        self.config.migration_type = orm.MigrationType.DELTA
        worker = queuer.QueueChunksWorker(self.config, self.redis)
        worker.min_id = 0
        worker.max_id = 100
        worker.num_rows = 80
        worker.queue_chunks()
        self.assertEqual(worker.c.chunk_size, 34)
        self.assertEqual(worker.num_chunks, 3)

    def test_queue_chunks_bad_type(self):
        self.mox.StubOutWithMock(queuer.orm, 'Chunk')

        ttc = self.mox.CreateMockAnything()
        ttc._cols().AndReturn([])
        orm.Chunk(self.redis).AndReturn(ttc)
        ttc.insert()

        self.mox.ReplayAll()
        config.CHUNK_SIZE = 30
        self.config.migration_type = '__UNKNOWN__'
        worker = queuer.QueueChunksWorker(self.config, self.redis)
        worker.min_id = 0
        worker.max_id = 100
        worker.num_rows = 80
        with self.assertRaises(queuer.UnrecoverableError):
            worker.queue_chunks()

    def test_get_table_metadata_full(self):
        self.mox.StubOutWithMock(queuer.db, 'shard_connection')
        conn = self.mox.CreateMockAnything()
        queuer.db.shard_connection('src', read=True).AndReturn(self.context(conn))
        self.mox.StubOutWithMock(queuer.db, 'cursor')
        cur = self.mox.CreateMockAnything()
        conn.get_current_timestamp().AndReturn(1)
        self.tt.update()
        self.mox.StubOutWithMock(queuer.QueueChunksWorker, 'get_column_metadata')
        queuer.QueueChunksWorker.get_column_metadata(conn)
        db.cursor(conn).AndReturn(self.context(cur))
        cur.execute(mox.IgnoreArg(), mox.IgnoreArg())
        cur.fetchone().AndReturn((1, 2, 3))

        self.mox.ReplayAll()
        self.config.migration_type = orm.MigrationType.FULL
        worker = queuer.QueueChunksWorker(self.config, self.redis)
        worker.get_table_metadata()

    def test_get_table_metadata_delta(self):
        self.config.delta_start = 12345
        self.mox.StubOutWithMock(queuer.db, 'shard_connection')
        conn = self.mox.CreateMockAnything()
        queuer.db.shard_connection('src', read=True).AndReturn(self.context(conn))
        self.mox.StubOutWithMock(queuer.db, 'cursor')
        cur = self.mox.CreateMockAnything()
        conn.get_current_timestamp().AndReturn(1)
        self.tt.update()
        self.mox.StubOutWithMock(queuer.QueueChunksWorker, 'get_column_metadata')
        queuer.QueueChunksWorker.get_column_metadata(conn)
        conn.from_unixtime_value(12345).AndReturn('2042T')

        db.cursor(conn).AndReturn(self.context(cur))
        cur.execute(mox.IgnoreArg(), mox.IgnoreArg())
        cur.fetchone().AndReturn((1, 2, 3))

        self.mox.ReplayAll()
        self.config.migration_type = orm.MigrationType.DELTA
        worker = queuer.QueueChunksWorker(self.config, self.redis)
        worker.column_map = {'a': {}, 'b': {}, 'c': {}}
        worker.get_table_metadata()
