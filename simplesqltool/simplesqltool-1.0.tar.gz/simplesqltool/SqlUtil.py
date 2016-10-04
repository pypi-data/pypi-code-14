import MySQLdb


class SQLAccess:
    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='1234', db=None, charset='utf8', use_unicode=True):
        self._con = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset, use_unicode=use_unicode)

    def selectall(self, tablename):
        cur = self._con.cursor()
        cur.execute('select * from {}'.format(tablename))
        return CursorManager(cur, cur.fetchall())

    def query(self, q):
        cur = self._con.cursor()
        cur.execute(q)
        return CursorManager(cur, cur.fetchall())

    def executeSql(self, sql):
        cur = self._con.cursor()
        cur.execute(sql)
        self._con.commit()
        return CursorManager(cur, None)


class CursorManager:
    def __init__(self, cursor, result):
        self._cursor = cursor
        self._result = result

    def __enter__(self):
        return self._result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.close()
