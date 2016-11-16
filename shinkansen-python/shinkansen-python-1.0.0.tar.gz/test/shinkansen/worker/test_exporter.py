import logging
import subprocess

import mox

from shinkansen import config, data, db, worker
from shinkansen.worker.exporter import mysql as exporter_mysql


class TestableExportChunkWorker(exporter_mysql.ExportChunkWorkerMysql):
    def __init__(self, chunk_config, chunk):
        # we don't want to test BaseChunkWorker.__init__ here so override it here
        self.c = chunk_config
        self.chunk = chunk
        self.logger = logging.getLogger(__name__)


class TestExporter(mox.MoxTestBase):
    def context(self, val=None):
        ctx = self.mox.CreateMockAnything()
        ctx.__enter__().AndReturn(val)
        ctx.__exit__(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        return ctx

    def setUp(self):
        super(TestExporter, self).setUp()
        config.SOURCES = {
            'src': {'type': 'mysql', 'config': {'read_host': {'host': 'HOST'}}},
        }
        config.DESTINATIONS = {
            'dst': {'type': 'crate'},
        }
        self.config = worker.ChunkConfig(
            migration_id='mid',
            table_config=data.TableConfig('tbl', 'tc', 'cc', None),
            columns=[],
            partition_val=43,
            namespace='ns',
            source_shard='src',
            destination_shard='dst',
            chunk_num=0,
            start_id=0,
            chunk_size=1,
        )
        self.chunk = self.mox.CreateMockAnything()
        self.worker = TestableExportChunkWorker(self.config, self.chunk)

    def test_run_only_mysql(self):
        self.mox.StubOutWithMock(exporter_mysql, 'time')
        exporter_mysql.time.sleep(mox.IgnoreArg())
        self.config.source_type = 'UNKNOWN'
        self.mox.ReplayAll()
        with self.assertRaises(worker.UnrecoverableError):
            self.worker._run()

    def test_run_proc_fails(self):
        self.mox.StubOutWithMock(exporter_mysql, 'time')
        exporter_mysql.time.sleep(mox.IgnoreArg())
        exporter_mysql.time.time().AndReturn(42)
        self.chunk.update()
        self.mox.StubOutWithMock(db, 'shard_connection')
        conn = self.mox.CreateMockAnything()
        db.shard_connection('src', read=True).AndReturn(self.context(conn))
        self.mox.StubOutWithMock(subprocess, 'Popen')
        proc = self.mox.CreateMockAnything()
        subprocess.Popen(mox.IgnoreArg(), shell=True, stdin=subprocess.PIPE).AndReturn(proc)
        proc.stdin = self.mox.CreateMockAnything()
        proc.stdin.close()
        proc.wait()
        proc.returncode = 1
        self.mox.ReplayAll()
        with self.assertRaises(exporter_mysql.CommandException):
            self.worker._run()

    def test_run(self):
        self.mox.StubOutWithMock(exporter_mysql, 'time')
        exporter_mysql.time.sleep(mox.IgnoreArg())
        exporter_mysql.time.time().AndReturn(42)
        self.chunk.update()
        self.mox.StubOutWithMock(db, 'shard_connection')
        conn = self.mox.CreateMockAnything()
        db.shard_connection('src', read=True).AndReturn(self.context(conn))
        self.mox.StubOutWithMock(subprocess, 'Popen')
        proc = self.mox.CreateMockAnything()
        subprocess.Popen(mox.IgnoreArg(), shell=True, stdin=subprocess.PIPE).AndReturn(proc)
        proc.stdin = self.mox.CreateMockAnything()
        proc.stdin.close()
        proc.wait()
        proc.returncode = 0
        self.mox.StubOutWithMock(db, 'cursor')
        cur = self.mox.CreateMockAnything()
        db.cursor(conn).AndReturn(self.context(cur))
        cur.execute(mox.IgnoreArg(), mox.IgnoreArg())
        cur.rowcount = 1
        self.mox.StubOutWithMock(exporter_mysql.streamer, 'queue_stream_chunk')
        exporter_mysql.streamer.queue_stream_chunk(self.config)
        self.chunk.update()
        self.chunk.update_status('exported', where_status='exporting')
        proc = self.mox.CreateMockAnything()
        subprocess.Popen(mox.IgnoreArg(), shell=True, stdin=subprocess.PIPE).AndReturn(proc)
        proc.stdin = self.mox.CreateMockAnything()
        proc.stdin.close()
        proc.wait()
        self.mox.ReplayAll()
        self.worker._run()
