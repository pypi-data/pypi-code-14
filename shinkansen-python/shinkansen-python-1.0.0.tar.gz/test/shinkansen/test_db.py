import crate.client.connection
import crate.client.cursor
import mox
import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor

import shinkansen
import shinkansen.db
from shinkansen import config


class TestException(Exception):
    pass


class CloseException(Exception):
    pass


class TestDB(mox.MoxTestBase):
    def setUp(self):
        super(TestDB, self).setUp()
        config.MYSQL_SHARDS = {
            'mysql': {
                'read_host': {'read': True},
                'write_host': {'write': True},
            },
        }
        config.CRATE_SHARDS = {
            'crate': {
            },
        }

    def test_shard_connection_closed_crate(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('crate', timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.close()
        self.mox.ReplayAll()

        with shinkansen.db.shard_connection('crate', False) as retconn:
            self.assertEqual(retconn._conn, conn)

    def test_shard_connection_closed_mysql_read(self):
        conn = self.mox.CreateMock(mysql.connector.connection.MySQLConnection)
        self.mox.StubOutWithMock(mysql.connector, 'connect')
        mysql.connector.connect(read=True, connection_timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.close()
        self.mox.ReplayAll()

        with shinkansen.db.shard_connection('mysql', True) as retconn:
            self.assertEqual(retconn._conn, conn)

    def test_shard_connection_closed_mysql_write(self):
        conn = self.mox.CreateMock(mysql.connector.connection.MySQLConnection)
        self.mox.StubOutWithMock(mysql.connector, 'connect')
        mysql.connector.connect(write=True, connection_timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.close()
        self.mox.ReplayAll()

        with shinkansen.db.shard_connection('mysql', False) as retconn:
            self.assertEqual(retconn._conn, conn)

    def test_shard_connection_unknown_shard(self):
        with self.assertRaises(shinkansen.UnrecoverableError):
            with shinkansen.db.shard_connection('unknown', False):
                raise TestException('This should not happen')

    def test_shard_connection_closed_on_exception(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('crate', timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.close()
        self.mox.ReplayAll()

        with self.assertRaises(TestException):
            with shinkansen.db.shard_connection('crate', False):
                raise TestException()

    def test_shard_connection_exception_on_close_is_raised(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('crate', timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.close().AndRaise(CloseException())
        self.mox.ReplayAll()

        with self.assertRaises(CloseException):
            with shinkansen.db.shard_connection('crate', False):
                pass

    def test_shard_connection_exception_on_close_after_exception_is_not_raised(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('crate', timeout=mox.IgnoreArg()).AndReturn(conn)
        conn.close().AndRaise(CloseException())
        self.mox.ReplayAll()

        with self.assertRaises(TestException):
            with shinkansen.db.shard_connection('crate', False):
                raise TestException()

    def test_cursor_closed(self):
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        cur = self.mox.CreateMock(mysql.connector.cursor.MySQLCursor)
        conn.cursor().AndReturn(cur)
        cur.close()
        self.mox.ReplayAll()

        with shinkansen.db.cursor(conn) as retcur:
            self.assertEqual(retcur, cur)

    def test_cursor_closed_on_exception(self):
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        cur = self.mox.CreateMock(mysql.connector.cursor.MySQLCursor)
        conn.cursor().AndReturn(cur)
        cur.close()
        self.mox.ReplayAll()

        with self.assertRaises(TestException):
            with shinkansen.db.cursor(conn):
                raise TestException()

    def test_cursor_exception_on_close_is_raised(self):
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        cur = self.mox.CreateMock(mysql.connector.cursor.MySQLCursor)
        conn.cursor().AndReturn(cur)
        cur.close().AndRaise(CloseException())
        self.mox.ReplayAll()

        with self.assertRaises(CloseException):
            with shinkansen.db.cursor(conn) as retcur:
                self.assertEqual(retcur, cur)

    def test_cursor_exception_on_close_after_exception_is_not_raised(self):
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        cur = self.mox.CreateMock(mysql.connector.cursor.MySQLCursor)
        conn.cursor().AndReturn(cur)
        cur.close().AndRaise(CloseException())
        self.mox.ReplayAll()

        with self.assertRaises(TestException):
            with shinkansen.db.cursor(conn):
                raise TestException()

    def test_shard_cursor_cursor_and_connection_closed(self):
        self.mox.StubOutWithMock(shinkansen.db, 'crate_conn')
        conn = self.mox.CreateMock(crate.client.connection.Connection)
        shinkansen.db.crate_conn('crate', timeout=mox.IgnoreArg()).AndReturn(conn)
        cur = self.mox.CreateMock(mysql.connector.cursor.MySQLCursor)
        conn.cursor().AndReturn(cur)
        cur.close()
        conn.close()
        self.mox.ReplayAll()

        with shinkansen.db.shard_cursor('crate', False) as retcur:
            self.assertEqual(retcur, cur)
