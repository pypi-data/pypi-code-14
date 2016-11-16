import logging
import subprocess

import crate.client.connection
import crate.client.cursor
import mox
import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor

import shinkansen.db
from shinkansen import config, data, orm, worker
from shinkansen.worker import importer, verifier


class TestableImportChunkWorker(importer.ImportChunkWorker):
    def __init__(self, chunk_config):
        # we don't want to test BaseChunkWorker.__init__ here so override it here
        self.c = chunk_config
        self.logger = logging.getLogger(__name__)


class TestException(Exception):
    pass


class TestImporterCrate(mox.MoxTestBase):
    def setUp(self):
        super(TestImporterCrate, self).setUp()
        config.SOURCES = {
            'src': {'type': 'mysql'},
        }
        config.DESTINATIONS = {
            'dst': {'type': 'crate'},
        }
        config.CRATE_SHARDS = {
            'dst': {},
        }
        self.config = worker.ChunkConfig(
            'mid', data.TableConfig('tbl', 'tc', 'cc', None), [],
            43, 'ns', 'src', 'dst',
            0, 0, 1, 1
        )

    def test_import_to_crate(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('dst', timeout=mox.IgnoreArg()).AndReturn(conn)
        cur = self.mox.CreateMock(crate.client.cursor.Cursor)
        conn.cursor().AndReturn(cur)
        cur.execute(mox.IgnoreArg())
        cur.rowcount = 42
        conn.commit()
        cur.close()
        conn.close()
        self.mox.ReplayAll()

        import_worker = TestableImportChunkWorker(self.config)
        import_worker._import_to_crate()
        self.assertEqual(self.config.num_records_imported, 42)

    def test_import_to_crate_connection_always_closed(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('dst', timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.cursor().AndRaise(TestException('test'))
        conn.close()
        self.mox.ReplayAll()

        import_worker = TestableImportChunkWorker(self.config)
        with self.assertRaises(TestException):
            import_worker._import_to_crate()

    def test_import_to_crate_cursor_always_closed(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('dst', timeout=mox.IgnoreArg()).AndReturn(conn)
        cur = self.mox.CreateMock(crate.client.cursor.Cursor)
        conn.cursor().AndReturn(cur)
        cur.execute(mox.IgnoreArg()).AndRaise(TestException('test'))
        cur.close()
        conn.close()
        self.mox.ReplayAll()

        import_worker = TestableImportChunkWorker(self.config)
        with self.assertRaises(TestException):
            import_worker._import_to_crate()


class TestImporterMysql(mox.MoxTestBase):
    def setUp(self):
        super(TestImporterMysql, self).setUp()
        config.SOURCES = {
            'src': {'type': 'mysql'},
        }
        config.DESTINATIONS = {
            'dst': {'type': 'mysql', 'config': {'write_host': {}}},
        }
        config.MYSQL_SHARDS = {
            'dst': {'read_host': {}, 'write_host': {}},
        }
        self.config = worker.ChunkConfig(
            'mid', data.TableConfig('tbl', 'tc', 'cc', None), [],
            43, 'ns', 'src', 'dst',
            0, 0, 1, 1
        )

    def test_import_to_mysql(self):
        self.mox.StubOutWithMock(mysql.connector, 'connect')
        conn = self.mox.CreateMock(mysql.connector.connection.MySQLConnection)
        mysql.connector.connect(connection_timeout=mox.IgnoreArg()).AndReturn(conn)
        cur = self.mox.CreateMock(mysql.connector.cursor.MySQLCursor)
        conn.cursor().AndReturn(cur)
        cur.execute(mox.IgnoreArg())
        cur.rowcount = 42
        conn.commit()
        cur.close()
        conn.close()
        self.mox.ReplayAll()

        import_worker = TestableImportChunkWorker(self.config)
        import_worker._import_to_mysql()
        self.assertEqual(self.config.num_records_imported, 42)

    def test_import_to_mysql_connection_always_closed(self):
        self.mox.StubOutWithMock(mysql.connector, 'connect')
        conn = self.mox.CreateMock(mysql.connector.connection.MySQLConnection)
        mysql.connector.connect(connection_timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.cursor().AndRaise(TestException('test'))
        conn.close()
        self.mox.ReplayAll()

        import_worker = TestableImportChunkWorker(self.config)
        with self.assertRaises(TestException):
            import_worker._import_to_mysql()

    def test_import_to_mysql_cursor_always_closed(self):
        self.mox.StubOutWithMock(mysql.connector, 'connect')
        conn = self.mox.CreateMock(mysql.connector.connection.MySQLConnection)
        mysql.connector.connect(connection_timeout=mox.IgnoreArg()).AndReturn(conn)
        cur = self.mox.CreateMock(mysql.connector.cursor.MySQLCursor)
        conn.cursor().AndReturn(cur)
        cur.execute(mox.IgnoreArg()).AndRaise(TestException('test'))
        cur.close()
        conn.close()
        self.mox.ReplayAll()

        import_worker = TestableImportChunkWorker(self.config)
        with self.assertRaises(TestException):
            import_worker._import_to_mysql()


class TestImportChunkWorker(mox.MoxTestBase):
    def setUp(self):
        super(TestImportChunkWorker, self).setUp()
        config.SOURCES = {
            'src': {'type': 'mysql', 'config': {}},
        }
        config.DESTINATIONS = {
            'dst': {'type': 'mysql', 'config': {'write_host': {}}},
        }
        config.ENABLE_VERIFIER = True
        self.config = worker.ChunkConfig(
            'mid',
            data.TableConfig('tbl', 'tc', 'cc', None), [],
            43, 'ns', 'src', 'dst',
            0, 0, 1, 1
        )

    def test_run_mysql(self):
        self.config.num_records_converted = 1
        import_worker = TestableImportChunkWorker(self.config)
        import_worker.chunk = self.mox.CreateMock(orm.Chunk)
        import_worker.chunk.update()
        self.mox.StubOutWithMock(import_worker, '_import_to_mysql')
        import_worker._import_to_mysql()
        import_worker.chunk.update()
        self.mox.StubOutWithMock(verifier, 'queue_verification')
        verifier.queue_verification(self.config)
        self.mox.StubOutClassWithMocks(subprocess, 'Popen')
        proc = subprocess.Popen(mox.IgnoreArg(), shell=True, stdin=subprocess.PIPE)
        proc.stdin = self.mox.CreateMockAnything()
        proc.stdin.close()
        proc.wait()
        proc.returncode = 0
        self.mox.ReplayAll()
        import_worker._run()

    def test_run_crate(self):
        self.config.num_records_converted = 1
        self.config.destination_type = 'crate'
        import_worker = TestableImportChunkWorker(self.config)
        import_worker.chunk = self.mox.CreateMock(orm.Chunk)
        import_worker.chunk.update()
        self.mox.StubOutWithMock(import_worker, '_import_to_crate')
        import_worker._import_to_crate()
        import_worker.chunk.update()
        self.mox.StubOutWithMock(verifier, 'queue_verification')
        verifier.queue_verification(self.config)
        self.mox.StubOutClassWithMocks(subprocess, 'Popen')
        proc = subprocess.Popen(mox.IgnoreArg(), shell=True, stdin=subprocess.PIPE)
        proc.stdin = self.mox.CreateMockAnything()
        proc.stdin.close()
        proc.wait()
        proc.returncode = 0
        self.mox.ReplayAll()
        import_worker._run()

    def test_run_unknown(self):
        self.config.num_records_converted = 1
        self.config.destination_type = 'UNKNOWN'
        import_worker = TestableImportChunkWorker(self.config)
        import_worker.chunk = self.mox.CreateMock(orm.Chunk)
        import_worker.chunk.update()
        self.mox.ReplayAll()
        with self.assertRaises(importer.Error):
            import_worker._run()

    def test_run_no_records(self):
        self.config.num_records_converted = 0
        import_worker = TestableImportChunkWorker(self.config)
        import_worker.chunk = self.mox.CreateMock(orm.Chunk)
        import_worker.chunk.update()
        self.mox.StubOutWithMock(verifier, 'queue_verification')
        verifier.queue_verification(self.config)
        self.mox.StubOutClassWithMocks(subprocess, 'Popen')
        proc = subprocess.Popen(mox.IgnoreArg(), shell=True, stdin=subprocess.PIPE)
        proc.stdin = self.mox.CreateMockAnything()
        proc.stdin.close()
        proc.wait()
        proc.returncode = 0
        self.mox.ReplayAll()
        import_worker._run()

    def test_run_removal_fails(self):
        self.config.num_records_converted = 0
        import_worker = TestableImportChunkWorker(self.config)
        import_worker.chunk = self.mox.CreateMock(orm.Chunk)
        import_worker.chunk.update()
        self.mox.StubOutWithMock(verifier, 'queue_verification')
        verifier.queue_verification(self.config)
        self.mox.StubOutClassWithMocks(subprocess, 'Popen')
        proc = subprocess.Popen(mox.IgnoreArg(), shell=True, stdin=subprocess.PIPE)
        proc.stdin = self.mox.CreateMockAnything()
        proc.stdin.close()
        proc.wait()
        proc.returncode = 1
        # Note that we do not get an exception in this case, it is only logged in order to make
        # this task idempotent.
        self.mox.ReplayAll()
        import_worker._run()
