import mox

from shinkansen.http import v5


class TestGetMigrationStatus(mox.MoxTestBase):
    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def setUp(self):
        super(TestGetMigrationStatus, self).setUp()
        v5.config.MIGRATION_REDIS_HOST = 'redis'
        self.mox.StubOutWithMock(v5.db, 'shard_connection')
        self.mox.StubOutWithMock(v5.db, 'redis_conn')
        self.mox.StubOutWithMock(v5.orm.Migration, 'get')
        self.mox.StubOutWithMock(v5.shinkansen.status, 'get_migration_status')
        self.redis = self.mox.CreateMockAnything()
        v5.db.redis_conn().AndReturn(self.context(self.redis))

    def test_None(self):
        v5.orm.Migration.get(self.redis, migration_id='MID').AndReturn(None)
        self.mox.ReplayAll()
        self.assertIsNone(v5.get_migration_status('MID'))

    def test_not_started(self):
        migration = self.mox.CreateMock(v5.orm.Migration)
        migration.migration_id = 'MID'
        migration.type = 'TYPE'
        migration.source_shard = 'src'
        migration.destination_shard = 'dst'
        migration.namespace = 'ns'
        migration.status = 'not_started'
        migration.partition_val = 'TID'
        migration.verification_status = ''
        migration.start_time = 1234
        migration.end_time = None
        v5.orm.Migration.get(self.redis, migration_id='MID').AndReturn(migration)
        v5.shinkansen.status.get_migration_status(migration_id='MID').AndReturn(
            v5.shinkansen.status.MigrationStatus(
                'not_started', '',
                {'ok': 1, 'not_ok': 2},
                {'ok': 2, 'not_ok': 1},
                {'ok': 1, 'not_ok': 3},
            )
        )
        self.mox.ReplayAll()
        self.assertEqual(
            v5.get_migration_status('MID'),
            {
                'migration_id': 'MID',
                'type': 'TYPE',
                'source': 'src',
                'destination': 'dst',
                'namespace': 'ns',
                'status': 'not_started',
                'status_code': 0,
                'partition_val': 'TID',
                'verification_status': '',
                'computed_status': 'not_started',
                'computed_status_code': 0,
                'computed_verification_status': '',
                'start_time': 1234,
                'end_time': None,
                'chunks_not_ok': 2,
                'chunks_ok': 1,
                'table_verifications_not_ok': 3,
                'table_verifications_ok': 1,
                'tables_not_ok': 1,
                'tables_ok': 2,
            }
        )

    def test_container(self):
        migration = self.mox.CreateMock(v5.orm.Migration)
        migration.migration_id = 'MID'
        migration.type = v5.orm.MigrationType.COMPLETE
        migration.source_shard = 'src'
        migration.destination_shard = 'dst'
        migration.namespace = 'ns'
        migration.status = 'in_progress'
        migration.partition_val = 'TID'
        migration.verification_status = ''
        migration.start_time = 1234
        migration.end_time = None

        sub1 = self.mox.CreateMock(v5.orm.Migration)
        sub1.migration_id = 'MID1'
        sub1.type = v5.orm.MigrationType.FULL
        sub1.source_shard = 'src'
        sub1.destination_shard = 'dst'
        sub1.namespace = 'ns'
        sub1.status = 'in_progress'
        sub1.partition_val = 'TID'
        sub1.verification_status = ''
        sub1.start_time = 1234
        sub1.end_time = None

        sub2 = self.mox.CreateMock(v5.orm.Migration)
        sub2.migration_id = 'MID2'
        sub2.type = v5.orm.MigrationType.AUTODELTA
        sub2.source_shard = 'src'
        sub2.destination_shard = 'dst'
        sub2.namespace = 'ns'
        sub2.status = 'in_progress'
        sub2.partition_val = 'TID'
        sub2.verification_status = ''
        sub2.start_time = 1234
        sub2.end_time = None
        v5.orm.Migration.get(self.redis, migration_id='MID').AndReturn(migration)
        v5.shinkansen.status.get_migration_status(migration_id='MID').AndReturn(
            v5.shinkansen.status.MigrationStatus(
                'in_progress', '',
                {}, {}, {}
            )
        )
        migration.get_submigrations().AndReturn([sub1, sub2])
        v5.shinkansen.status.get_migration_status(migration_id='MID1').AndReturn(
            v5.shinkansen.status.MigrationStatus(
                'in_progress', '',
                {}, {}, {}
            )
        )
        v5.shinkansen.status.get_migration_status(migration_id='MID2').AndReturn(
            v5.shinkansen.status.MigrationStatus(
                'in_progress', '',
                {}, {}, {}
            )
        )
        self.maxDiff = None
        sub2.get_submigrations().AndReturn([])
        self.mox.ReplayAll()
        self.assertEqual(
            v5.get_migration_status('MID'),
            {
                'migration_id': 'MID',
                'type': 'complete',
                'source': 'src',
                'destination': 'dst',
                'namespace': 'ns',
                'status': 'in_progress',
                'status_code': 2,
                'partition_val': 'TID',
                'verification_status': '',
                'computed_status': 'in_progress',
                'computed_status_code': 2,
                'computed_verification_status': '',
                'start_time': 1234,
                'end_time': None,
                'links': [{'href': '/v5/migration/MID/tables',
                           'method': 'GET',
                           'rel': 'tables'}],
                'submigrations': [{'computed_status': 'in_progress',
                                   'computed_status_code': 2,
                                   'computed_verification_status': '',
                                   'destination': 'dst',
                                   'end_time': None,
                                   'links': [{'href': '/v5/migration/MID1/tables',
                                              'method': 'GET',
                                              'rel': 'tables'}],
                                   'migration_id': 'MID1',
                                   'namespace': 'ns',
                                   'source': 'src',
                                   'start_time': 1234,
                                   'status': 'in_progress',
                                   'status_code': 2,
                                   'partition_val': 'TID',
                                   'type': 'full',
                                   'verification_status': ''},
                                  {'computed_status': 'in_progress',
                                   'computed_status_code': 2,
                                   'computed_verification_status': '',
                                   'destination': 'dst',
                                   'end_time': None,
                                   'links': [{'href': '/v5/migration/MID2/tables',
                                              'method': 'GET',
                                              'rel': 'tables'}],
                                   'migration_id': 'MID2',
                                   'namespace': 'ns',
                                   'source': 'src',
                                   'start_time': 1234,
                                   'status': 'in_progress',
                                   'status_code': 2,
                                   'submigrations': [],
                                   'partition_val': 'TID',
                                   'type': 'autodelta',
                                   'verification_status': ''}],
            }
        )
