import logging

import mox

from shinkansen import config, data, worker
from shinkansen.worker import pipe


class TestablePipeChunkWorker(pipe.PipeChunkWorker):
    def __init__(self, chunk_config, chunk):
        # we don't want to test BaseChunkWorker.__init__ here so override it here
        self.c = chunk_config
        self.chunk = chunk
        self.redis_conn = None
        self.logger = logging.getLogger(__name__)


class TestPipe(mox.MoxTestBase):
    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def setUp(self):
        super(TestPipe, self).setUp()
        config.SOURCES = {
            'src': {'type': 'mysql', 'config': {'read_host': {'host': 'HOST'}}},
        }
        config.DESTINATIONS = {
            'dst': {'type': 'crate'},
        }
        config.ENABLE_VERIFIER = True
        config.PIPE_BULK_INSERT_SIZE = 42
        self.config = worker.ChunkConfig(
            'mid', data.TableConfig('tbl', 'tc', 'cc', None), [],
            43, 'ns', 'src', 'dst',
            0, 0, 1, 1
        )
        self.chunk = self.mox.CreateMockAnything()
        self.worker = TestablePipeChunkWorker(self.config, self.chunk)

    # def test_run(self):
    #     self.chunk.update()
    #     self.mox.StubOutWithMock(pipe.db, 'shard_connection')
    #     src_conn = self.mox.CreateMockAnything()
    #     pipe.db.shard_connection('src', read=True).AndReturn(self.context(src_conn))
    #     dst_conn = self.mox.CreateMockAnything()
    #     pipe.db.shard_connection('dst', read=False).AndReturn(self.context(dst_conn))
    #     self.mox.StubOutWithMock(self.worker, 'migrate')
    #     self.worker.migrate(src_conn, dst_conn)
    #     self.chunk.update()
    #     self.mox.StubOutWithMock(pipe.status, 'get_migration_status')
    #     pipe.status.get_migration_status(migration_id='mid').AndReturn(
    #         ('mst', None, None, None, None)
    #     )
    #     self.mox.StubOutWithMock(pipe.orm.Migration, 'get')
    #     migration = self.mox.CreateMockAnything()
    #     pipe.orm.Migration.get(None, migration_id='mid').AndReturn(migration)
    #     migration.update()
    #     self.mox.StubOutWithMock(pipe.verifier, 'queue_verification')
    #     pipe.verifier.queue_verification(self.config)
    #     self.mox.ReplayAll()
    #     self.worker._run()

    # def test_migrate(self):
    #     self.mox.StubOutWithMock(pipe.db, 'cursor')
    #     cur = self.mox.CreateMockAnything()
    #     pipe.db.cursor(None).AndReturn(self.context(cur))
    #     cur.execute(mox.IgnoreArg())
    #     cur.fetchmany(42).AndReturn([1, 2, 3])
    #     self.chunk.update()
    #     self.mox.StubOutWithMock(self.worker, 'upsert')
    #     self.worker.upsert(None, [1, 2, 3])
    #     cur.fetchmany(42).AndReturn(None)
    #     self.mox.ReplayAll()
    #     self.chunk.num_records_exported = 0
    #     self.worker.migrate(None, None)
    #     self.assertEqual(self.chunk.num_records_exported, 3)

    def test_upsert_failure(self):
        self.mox.StubOutWithMock(pipe.db, 'cursor')
        conn = self.mox.CreateMockAnything()
        conn.PARAMETER_PLACEHOLDER = '|'
        cur = self.mox.CreateMockAnything()
        pipe.db.cursor(conn).AndReturn(self.context(cur))
        cur.executemany(mox.IgnoreArg(), [1, 2, 3]).AndReturn([{'rowcount': -1}])
        self.chunk.update()
        self.mox.ReplayAll()
        self.chunk.num_records_imported = 0
        with self.assertRaises(pipe.Error):
            self.worker.upsert(conn, [1, 2, 3])

    def test_upsert(self):
        conn = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(pipe.db, 'cursor')
        cur = self.mox.CreateMockAnything()
        pipe.db.cursor(conn).AndReturn(self.context(cur))
        cur.executemany(mox.IgnoreArg(), [1, 2, 3]).AndReturn([{'rowcount': 2}])
        self.chunk.update()
        conn.commit()
        self.mox.ReplayAll()
        self.chunk.num_records_imported = 0
        self.worker.upsert(conn, [1, 2, 3])
        self.assertEqual(self.chunk.num_records_imported, 2)
