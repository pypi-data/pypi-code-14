import logging

import mox
import redlock.lock

import shinkansen
from shinkansen import config, data, orm, status, worker
from shinkansen.worker import queuer, verifier


class TestableVerifyWorker(verifier.VerifyWorker):
    def __init__(self, chunk_config):
        # we don't want to test BaseChunkWorker.__init__ here so override it here
        self.c = chunk_config
        self.redis_conn = object()
        self.logger = logging.getLogger(__name__)


class Context(object):
    def __enter__(self, *a, **k):
        pass

    def __exit__(self, *a, **k):
        pass


class TestVerifierBase(mox.MoxTestBase):
    def setUp(self):
        super(TestVerifierBase, self).setUp()
        config.SOURCES = {
            'src': {
                'type': 'mysql',
                'config': {
                    'tables': [
                        data.TableConfig('table', 'tcol', 'ccol', None),
                        data.TableConfig('table2', 'tcol2', 'ccol2', None),
                    ],
                },
            },
        }
        config.DESTINATIONS = {
            'dst': {'type': 'crate'},
        }
        self.chunk_config = worker.ChunkConfig(
            'mid', data.TableConfig('TableA', 'filter_col_a', 'chunk_col_a', None), None, 42,
            'ns', 'src', 'dst', None, None, None,
            'mysql', 'crate')
        self.mox.StubOutWithMock(status, 'get_migration_status')
        self.mox.StubOutWithMock(orm.Migration, 'get')
        self.mox.StubOutWithMock(orm.Migration, '_lock')
        self.migration = self.mox.CreateMock(orm.Migration)
        self.migration.migration_id = 'MID'
        self.migration.verification_status = ''
        self.worker = TestableVerifyWorker(self.chunk_config)
        self.lock = Context()

    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx


class TestVerifierRun(TestVerifierBase):
    def setUp(self):
        super(TestVerifierRun, self).setUp()
        orm.Migration._lock().AndReturn(self.lock)
        orm.Migration.get(self.worker.redis_conn, migration_id='mid').AndReturn(self.migration)

    def test_noop_until_finished(self):
        self.migration.update(lock=self.lock)
        status.get_migration_status(migration_id='mid').AndReturn(
            status.MigrationStatus('in_progress', 'pending', {}, {}, {}))
        self.mox.ReplayAll()
        self.worker._run()

    def test_exception_unsets_chunk(self):
        status.get_migration_status(migration_id='mid').AndRaise(Exception())
        self.mox.ReplayAll()
        with self.assertRaises(Exception):
            self.worker._run()
        self.assertIsNone(self.worker.chunk)

    def test_previously_verified_skipped(self):
        self.mox.ReplayAll()
        self.migration.verification_status = 'verified'
        self.worker._run()

    def test_previously_failed_skipped(self):
        self.mox.ReplayAll()
        self.migration.verification_status = 'failed'
        self.worker._run()

    def test_finished_is_verified(self):
        self.migration.update(lock=self.lock)
        status.get_migration_status(migration_id='mid').AndReturn(
            status.MigrationStatus('finished', 'pending', {}, {}, {}))
        self.mox.StubOutWithMock(self.worker, 'verify_migration')
        self.worker.verify_migration(self.migration, self.lock)
        self.mox.ReplayAll()
        self.worker._run()

    def test_empty_is_verified(self):
        self.migration.update(lock=self.lock)
        status.get_migration_status(migration_id='mid').AndReturn(
            status.MigrationStatus('empty', 'pending', {}, {}, {}))
        self.mox.StubOutWithMock(self.worker, 'verify_migration')
        self.worker.verify_migration(self.migration, self.lock)
        self.mox.ReplayAll()
        self.worker._run()


class TestVerifierRunRetry(TestVerifierBase):
    def test_retry_after_lock_error(self):
        self.lock = self.mox.CreateMockAnything()
        orm.Migration._lock().AndReturn(self.lock)
        self.lock.__enter__().AndRaise(redlock.lock.RedLockError())
        self.mox.ReplayAll()
        with self.assertRaises(worker.RetryException):
            self.worker._run()


class TestVerifyMigration(TestVerifierBase):
    def test_non_crate_delta(self):
        self.migration.type = orm.MigrationType.DELTA
        self.chunk_config.destination_type = 'UNKNOWN'
        with self.assertRaises(shinkansen.UnrecoverableError):
            self.worker.verify_migration(self.migration, self.lock)

    def test_container(self):
        self.migration.type = orm.MigrationType.AUTODELTA
        self.migration.parent_migration_id = 'PMID'
        self.mox.StubOutWithMock(self.worker, 'calculate_container_verification_status')
        self.worker.calculate_container_verification_status(self.migration).AndReturn('verified')
        self.migration.update(lock=self.lock)
        self.mox.StubOutWithMock(self.worker, 'handle_parent_migration')
        self.worker.handle_parent_migration(self.migration)
        self.mox.ReplayAll()
        self.worker.verify_migration(self.migration, self.lock)

    def test_leaf(self):
        self.migration.type = orm.MigrationType.FULL
        self.migration.parent_migration_id = None
        self.mox.StubOutWithMock(self.worker, 'calculate_verification_status')
        self.worker.calculate_verification_status(self.migration, {}).AndReturn('UNKNOWN')
        self.migration.update(lock=self.lock)
        self.mox.ReplayAll()
        self.worker.verify_migration(self.migration, self.lock)


class TestMissingParentMigration(TestVerifierBase):
    def test_missing_parent_migration(self):
        self.migration.parent_migration_id = 'PMID'
        orm.Migration.get(self.worker.redis_conn, migration_id='PMID').AndReturn(None)
        self.mox.ReplayAll()
        with self.assertRaises(shinkansen.UnrecoverableError):
            self.worker.handle_parent_migration(self.migration)


class TestHandleParentMigration(TestVerifierBase):
    def setUp(self):
        super(TestHandleParentMigration, self).setUp()
        self.migration.parent_migration_id = 'PMID'
        self.parent_migration = self.mox.CreateMock(orm.Migration)
        orm.Migration.get(self.worker.redis_conn, migration_id='PMID').AndReturn(
            self.parent_migration)
        self.mox.StubOutWithMock(self.worker, 'queue_migration_verification')

    def test_handle_parent_migration_unfinished(self):
        self.migration.status = 'in_progress'
        self.worker.queue_migration_verification(self.parent_migration)
        self.mox.ReplayAll()
        self.worker.handle_parent_migration(self.migration)

    def test_handle_parent_migration_autodelta(self):
        self.migration.status = 'finished'
        self.parent_migration.type = orm.MigrationType.AUTODELTA
        self.mox.StubOutWithMock(self.worker, 'handle_parent_autodelta')
        self.worker.handle_parent_autodelta(self.migration, self.parent_migration)
        self.mox.ReplayAll()
        self.worker.handle_parent_migration(self.migration)

    def test_handle_parent_migration_complete(self):
        self.migration.status = 'finished'
        self.parent_migration.type = orm.MigrationType.COMPLETE
        self.mox.StubOutWithMock(self.worker, 'handle_parent_complete')
        self.worker.handle_parent_complete(self.migration, self.parent_migration)
        self.mox.ReplayAll()
        self.worker.handle_parent_migration(self.migration)

    def test_handle_parent_migration_unknown(self):
        self.migration.status = 'empty'
        self.parent_migration.type = 'UNKNOWN'
        self.mox.ReplayAll()
        with self.assertRaises(shinkansen.UnrecoverableError):
            self.worker.handle_parent_migration(self.migration)


class TestHandleParentMigrationTypes(TestVerifierBase):
    def setUp(self):
        super(TestHandleParentMigrationTypes, self).setUp()
        self.migration.parent_migration_id = 'PMID'
        self.parent_migration = self.mox.CreateMock(orm.Migration)
        self.parent_migration.migration_id = 'PMID'
        self.mox.StubOutWithMock(self.worker, 'queue_migration_verification')
        self.mox.StubOutWithMock(queuer, 'migrate_partition_shard')
        self.parent_migration.partition_val = 'TID'
        self.parent_migration.namespace = 'ns'
        self.parent_migration.source_shard = 'src'
        self.parent_migration.destination_shard = 'dst'

    def test_handle_parent_autodelta_finished(self):
        self.migration.status = 'empty'
        self.worker.queue_migration_verification(self.parent_migration)
        self.mox.ReplayAll()
        self.worker.handle_parent_autodelta(self.migration, self.parent_migration)

    def test_handle_parent_autodelta_unfinished(self):
        self.migration.status = 'finished'
        queuer.migrate_partition_shard(
            'TID', 'ns', 'src', 'dst',
            force=False, requeue=False, migration_type=orm.MigrationType.DELTA,
            parent_migration_id='PMID', latest_migration=self.migration)
        self.mox.ReplayAll()
        self.worker.handle_parent_autodelta(self.migration, self.parent_migration)

    def test_handle_parent_complete_finished(self):
        self.migration.type = orm.MigrationType.AUTODELTA
        self.worker.queue_migration_verification(self.parent_migration)
        self.mox.ReplayAll()
        self.worker.handle_parent_complete(self.migration, self.parent_migration)

    def test_handle_parent_complete_unfinished(self):
        self.migration.type = orm.MigrationType.FULL
        self.migration.status = 'finished'
        queuer.migrate_partition_shard(
            'TID', 'ns', 'src', 'dst',
            force=False, requeue=False, migration_type=orm.MigrationType.AUTODELTA,
            parent_migration_id='PMID', latest_migration=self.migration)
        self.mox.ReplayAll()
        self.worker.handle_parent_complete(self.migration, self.parent_migration)


class TestQueueMigrationVerification(TestVerifierBase):
    def test_queue_migration_verification(self):
        self.migration.migration_id = 'MID'
        self.migration.partition_val = 'TID'
        self.migration.namespace = 'ns'
        self.migration.source_shard = 'src'
        self.migration.destination_shard = 'dst'
        self.migration.type = 'TYPE'
        self.mox.StubOutWithMock(verifier, 'queue_verification')
        chunk_config = shinkansen.worker.ChunkConfig(
            migration_id='MID',
            partition_val='TID',
            namespace='ns',
            source_shard='src',
            destination_shard='dst',
            source_schema='mysql',
            destination_schema='crate',
            migration_type='TYPE',
            table_config=None, columns=None, chunk_num=None, start_id=None, chunk_size=None,
        )
        verifier.queue_verification(chunk_config)
        self.mox.ReplayAll()
        self.worker.queue_migration_verification(self.migration)


class TestCalculateVerificationStatus(TestVerifierBase):
    def get_submigrations(self, verification_statuses):
        migrations = []
        for verification_status in verification_statuses:
            migration = self.mox.CreateMock(orm.Migration)
            migration.verification_status = verification_status
            migrations.append(migration)
        return migrations

    def setup_table_data(self, statuses, verification_statuses):
        self.migration.status = 'finished'
        self.mox.StubOutWithMock(verifier.db, 'shard_connection')
        conn = self.mox.CreateMockAnything()
        verifier.db.shard_connection('dst', read=False).AndReturn(self.context(conn))
        self.mox.StubOutWithMock(self.worker, 'check_table')
        i = 0
        for table_config in config.SOURCES['src']['config']['tables']:
            table_data = self.mox.CreateMock(orm.Table)
            table_data.status = statuses[min(i, len(statuses) - 1)]
            table_data.verification_status = verification_statuses[min(i, len(verification_statuses) - 1)]
            self.worker.check_table(table_config, conn).AndReturn(table_data)
            i += 1

    def test_calculate_container_verification_status_all_subs_same(self):
        self.migration.get_submigrations().AndReturn(self.get_submigrations(['MONO', 'MONO', 'MONO']))
        self.mox.ReplayAll()
        self.assertEqual(self.worker.calculate_container_verification_status(self.migration), 'MONO')

    def test_calculate_container_verification_status_failed(self):
        self.migration.get_submigrations().AndReturn(self.get_submigrations(['b', 'failed', 'a']))
        self.mox.ReplayAll()
        self.assertEqual(self.worker.calculate_container_verification_status(self.migration), 'failed')

    def test_calculate_container_verification_status_pending(self):
        self.migration.get_submigrations().AndReturn(self.get_submigrations(['b', 'c', 'a']))
        self.mox.ReplayAll()
        self.assertEqual(self.worker.calculate_container_verification_status(self.migration), 'pending')

    def test_calculate_verification_status_incorrect_table_status(self):
        self.setup_table_data(['empty', 'OTHER'], ['OTHER'])
        self.mox.ReplayAll()
        with self.assertRaises(verifier.Error):
            self.worker.calculate_verification_status(self.migration, {})

    def test_calculate_verification_status_all_same(self):
        self.setup_table_data(['chunks_queued', 'empty'], ['OTHER'])
        self.mox.ReplayAll()
        self.assertEqual(self.worker.calculate_verification_status(self.migration, {}), 'OTHER')

    def test_calculate_verification_status_ignore_unknown(self):
        self.setup_table_data(['chunks_queued', 'empty'], ['unknown', 'OTHER'])
        self.mox.ReplayAll()
        self.assertEqual(self.worker.calculate_verification_status(self.migration, {}), 'OTHER')

    def test_calculate_verification_status_failed(self):
        self.setup_table_data(['chunks_queued', 'empty'], ['A', 'OTHER'])
        self.mox.ReplayAll()
        self.assertEqual(self.worker.calculate_verification_status(self.migration, {}), 'failed')
