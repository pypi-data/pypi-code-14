import contextlib

import mox

import shinkansen
import shinkansen.db
from shinkansen import orm, status


@contextlib.contextmanager
def context(ret):
    yield ret


class TestGetMigrationStatus(mox.MoxTestBase):
    def _test_get_migration_status_base(
        self, table_status_recs, chunk_status_recs, table_verification_status_recs
    ):
        self.mox.StubOutWithMock(shinkansen.db, 'redis_conn')
        redis_conn = self.mox.CreateMockAnything()
        shinkansen.db.redis_conn().AndReturn(redis_conn)
        redis_conn.__enter__().AndReturn(redis_conn)

        ttrecs = []
        for num, table_status in table_status_recs:
            for i in xrange(num):
                tt = self.mox.CreateMock(orm.Table)
                tt.status = table_status
                tt.verification_status = table_verification_status_recs[0][1]
                ttrecs.append(tt)

        self.mox.StubOutWithMock(orm.Table, 'get_by_index')
        orm.Table.get_by_index(
            redis_conn,
            source_shard=mox.IgnoreArg(), destination_shard=mox.IgnoreArg(), partition_val=mox.IgnoreArg()).AndReturn(
            ttrecs)

        ttcrecs = []
        for num, chunk_status in chunk_status_recs:
            for i in xrange(num):
                ttc = self.mox.CreateMock(orm.Chunk)
                ttc.status = chunk_status
                ttcrecs.append(ttc)

        self.mox.StubOutWithMock(orm.Chunk, 'get_by_index')
        orm.Chunk.get_by_index(
            redis_conn,
            source_shard=mox.IgnoreArg(), destination_shard=mox.IgnoreArg(), partition_val=mox.IgnoreArg()).AndReturn(
            ttcrecs)

        redis_conn.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())

        self.mox.ReplayAll()

    def test_get_migration_status_no_partition(self):
        with self.assertRaises(shinkansen.UnrecoverableError):
            status.get_migration_status('src', 'dst', None)

    def test_get_migration_status_only_source(self):
        with self.assertRaises(shinkansen.UnrecoverableError):
            status.get_migration_status('src', None, 42)

    def test_get_migration_status_only_destination(self):
        with self.assertRaises(shinkansen.UnrecoverableError):
            status.get_migration_status(None, 'dst', 42)

    def _test_get_migration_status(
        self, table_status_recs, table_verification_status_recs, chunk_status_recs, expected
    ):
        self._test_get_migration_status_base(table_status_recs, table_verification_status_recs, chunk_status_recs)
        self.assertEqual(status.get_migration_status('src', 'dst', 42), expected)

    def test_get_migration_status_none(self):
        self._test_get_migration_status(
            [], [], [],
            ('not_started', 'pending', {}, {}, {}))

    def test_get_migration_status_all_empty_tables(self):
        self._test_get_migration_status(
            [(2, 'empty')], [], [(2, 'verified')],
            ('empty', 'verified', {}, {'empty': 2}, {'verified': 2}))

    def test_get_migration_status_all_queued_tables(self):
        self._test_get_migration_status(
            [(2, 'queued')], [], [(2, 'pending')],
            ('queued', 'pending', {}, {'queued': 2}, {'pending': 2}))

    def test_get_migration_status_all_queued_chunks(self):
        self._test_get_migration_status(
            [], [(2, 'queued')], [],
            ('queued', 'pending', {'queued': 2}, {}, {}))

    def test_get_migration_status_chunks_empty_and_queued(self):
        self._test_get_migration_status(
            [], [(2, 'queued'), (3, 'empty')], [],
            ('in_progress', 'pending', {'queued': 2, 'empty': 3}, {}, {}))

    def test_get_migration_status_all_chunks_imported(self):
        self._test_get_migration_status(
            [(2, 'chunks_queued')], [(2, 'imported')], [(2, 'verified')],
            ('finished', 'verified', {'imported': 2}, {'chunks_queued': 2}, {'verified': 2}))

    def test_get_migration_status_chunks_imported_and_empty(self):
        self._test_get_migration_status(
            [(2, 'chunks_queued')], [(2, 'imported'), (3, 'empty')], [(2, 'verified')],
            ('finished', 'verified', {'imported': 2, 'empty': 3}, {'chunks_queued': 2}, {'verified': 2}))


class TestGetTableMigrationStatus(mox.MoxTestBase):
    def _test_get_migration_status_base(self, table_status_recs, chunk_status_recs):
        self.mox.StubOutWithMock(shinkansen.db, 'redis_conn')
        redis_conn = self.mox.CreateMockAnything()
        shinkansen.db.redis_conn().AndReturn(redis_conn)
        redis_conn.__enter__().AndReturn(redis_conn)

        ttrecs = []
        for (
            table_name, table_status, num_chunks,
            chunk_size, min_id, max_id, num_records,
            verification_status
        ) in table_status_recs:
            tt = self.mox.CreateMock(orm.Table)
            tt.table_name = table_name
            tt.status = table_status
            tt.table_status = table_status
            tt.num_chunks = num_chunks
            tt.chunk_size = chunk_size
            tt.min_id = min_id
            tt.max_id = max_id
            tt.num_records = num_records
            tt.verification_status = verification_status
            tt.queued_time = 0
            tt.start_time = 0
            tt.end_time = 0
            tt.source_start_time = 0
            ttrecs.append(tt)

        self.mox.StubOutWithMock(orm.Table, 'get_by_index')
        orm.Table.get_by_index(
            redis_conn,
            source_shard=mox.IgnoreArg(), destination_shard=mox.IgnoreArg(), partition_val=mox.IgnoreArg()).AndReturn(
            ttrecs)

        ttcrecs = []
        for (
            table_name, chunk_status, num_chunks,
            exported, converted, imported,
            export_ms, convert_ms, import_ms
        ) in chunk_status_recs:
            for i in xrange(num_chunks):
                ttc = self.mox.CreateMock(orm.Chunk)
                ttc.table_name = table_name
                ttc.num_records_exported = exported
                ttc.num_records_converted = converted
                ttc.num_records_imported = imported
                ttc.export_elapsed_ms = export_ms
                ttc.import_elapsed_ms = import_ms
                ttc.convert_elapsed_ms = convert_ms
                ttc.status = chunk_status
                ttcrecs.append(ttc)
                exported = 0
                imported = 0
                converted = 0
                export_ms = 0
                import_ms = 0
                convert_ms = 0

        self.mox.StubOutWithMock(orm.Chunk, 'get_by_index')
        orm.Chunk.get_by_index(
            redis_conn,
            source_shard=mox.IgnoreArg(), destination_shard=mox.IgnoreArg(), partition_val=mox.IgnoreArg()).AndReturn(
            ttcrecs)

        redis_conn.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())

        self.mox.ReplayAll()

    def _test_get_table_migration_status(self, table_status_recs, chunk_status_recs, expected):
        self._test_get_migration_status_base(table_status_recs, chunk_status_recs)
        result = status.get_table_migration_status('src', 'dst', 43)
        self.assertEqual(result, expected)

    def test_get_table_migration_status_no_partition(self):
        with self.assertRaises(shinkansen.UnrecoverableError):
            status.get_table_migration_status('src', 'dst', None)

    def test_get_table_migration_status_only_source(self):
        with self.assertRaises(shinkansen.UnrecoverableError):
            status.get_table_migration_status('src', None, 42)

    def test_get_table_migration_status_only_destination(self):
        with self.assertRaises(shinkansen.UnrecoverableError):
            status.get_table_migration_status(None, 'dst', 42)

    def test_get_table_migration_status(self):
        self.maxDiff = None
        self._test_get_table_migration_status(
            [
                ('tbl', 'chunks_queued', 9, 11, 5, 12345, 4747, 'verified'),
                ('tbl2', 'queued', None, None, None, None, None, 'pending'),
            ],
            [
                ('tbl', 'exported', 2, 5, 0, 0, 6, 0, 0),
                ('tbl', 'converting', 3, 6, 6, 0, 7, 7, 0),
                ('tbl', 'imported', 4, 7, 7, 7, 8, 8, 8),
            ],
            {
                'tbl': {
                    'partition_val': 43,
                    'num_records_exported': 18,
                    'num_records_converted': 13,
                    'num_records_imported': 7,
                    'num_chunks': 9,
                    'export_elapsed_ms': 21,
                    'convert_elapsed_ms': 15,
                    'import_elapsed_ms': 8,
                    'chunk_size': 11,
                    'min_id': 5,
                    'max_id': 12345,
                    'num_records_total': 4747,
                    'num_chunks_exported': 2,
                    'num_chunks_converting': 3,
                    'num_chunks_imported': 4,
                    'status': 'chunks_queued',
                    'verification_status': 'verified',
                    'queued_time': 0,
                    'start_time': 0,
                    'end_time': 0,
                },
                'tbl2': {
                    'partition_val': 43,
                    'num_records_exported': 0,
                    'num_records_converted': 0,
                    'num_records_imported': 0,
                    'num_chunks': 0,
                    'export_elapsed_ms': 0,
                    'convert_elapsed_ms': 0,
                    'import_elapsed_ms': 0,
                    'chunk_size': 0,
                    'min_id': 0,
                    'max_id': 0,
                    'num_records_total': 0,
                    'status': 'queued',
                    'verification_status': 'pending',
                    'queued_time': 0,
                    'start_time': 0,
                    'end_time': 0,
                }
            }
        )


class TestContainerStatus(mox.MoxTestBase):
    def setUp(self):
        super(TestContainerStatus, self).setUp()
        self.migration = self.mox.CreateMock(orm.Migration)
        self.sub = self.mox.CreateMock(orm.Migration)
        self.migration.get_latest_submigration().AndReturn(self.sub)

    def test_autodelta_in_progress(self):
        self.sub.status = 'OTHER'
        self.mox.ReplayAll()
        self.assertEqual(status.get_autodelta_migration_status(self.migration).computed_status, 'in_progress')

    def test_autodelta_finished(self):
        self.sub.status = 'empty'
        self.mox.ReplayAll()
        self.assertEqual(status.get_autodelta_migration_status(self.migration).computed_status, 'finished')

    def test_complete_autodelta_queued(self):
        self.sub.type = orm.MigrationType.AUTODELTA
        self.sub.status = 'queued'
        self.mox.ReplayAll()
        self.assertEqual(status.get_complete_migration_status(self.migration).computed_status, 'in_progress')

    def test_complete_autodelta_other(self):
        self.sub.type = orm.MigrationType.AUTODELTA
        self.sub.status = 'OTHER'
        self.mox.ReplayAll()
        self.assertEqual(status.get_complete_migration_status(self.migration).computed_status, 'OTHER')

    def test_complete_other_other(self):
        self.sub.type = 'OTHER'
        self.sub.status = 'OTHER'
        self.mox.ReplayAll()
        self.assertEqual(status.get_complete_migration_status(self.migration).computed_status, 'OTHER')

    def test_complete_other_finished(self):
        self.sub.type = 'OTHER'
        self.sub.status = 'finished'
        self.mox.ReplayAll()
        self.assertEqual(status.get_complete_migration_status(self.migration).computed_status, 'in_progress')

    def test_complete_other_empty(self):
        self.sub.type = 'OTHER'
        self.sub.status = 'empty'
        self.mox.ReplayAll()
        self.assertEqual(status.get_complete_migration_status(self.migration).computed_status, 'in_progress')
