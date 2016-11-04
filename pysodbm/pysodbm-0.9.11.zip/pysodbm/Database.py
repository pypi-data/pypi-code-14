#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymysql.cursors import DictCursorMixin, Cursor

__author__ = 'Marco Bartel'

import platform
import pymysql
import warnings

warnings.filterwarnings('ignore', category=pymysql.Warning)

from pysodbm import *
# from profilehooks import profile, timecall
from multiprocessing import Lock
import datetime
import time

LOG = logging.getLogger(__name__)

class CustomDictCursorMixIn(DictCursorMixin):
    def _conv_row(self, row):
        if row is None:
            return None
        return self.dict_type(zip(self._fields, tuple(
            (datetime.datetime.min + i).time() if isinstance(i, datetime.timedelta) else i for i in row)))


class CustomDictCursor(CustomDictCursorMixIn, Cursor):
    pass


class DatabaseLock(object):
    def __init__(self):
        self._lock = Lock()
        self._locked = False

    def acquire(self):
        self._locked = True
        r = False
        while not r:
            r = self._lock.acquire(False)
            time.sleep(.01)

    def release(self):
        self._lock.release()
        self._locked = False

    def locked(self):
        return self._locked


class Database(object):
    RETURN_LIST = 0
    RETURN_DICT = 1
    RETURN_OBJECT = 2

    MAX_CONNECTIONS = 5

    LIST_CURSOR = 1
    DICT_CURSOR = 2

    connectionWatcher = None
    hooksEnabled = False
    systemName = "default"

    @staticmethod
    def dbEscapeString(mstr):
        return pymysql.escape_string(mstr)

    @classmethod
    def isWindows(cls):
        return True if platform.system().lower() == "windows" else False

    def __init__(self, config=None):
        self.config = config
        self.dbConnections = []
        self.dbLock = threading.Lock()
        self.dbName = ""

        self.connectionWatcher = DatabaseConnectionWatcher(db=self)
        self.connectionWatcher.start()


    def checkFieldExists(self, tableName="", fieldToCheck=[]):
        query = """
            show columns from %s
        """ % tableName

        existingTableFields = self.dbQueryDict(query)
        fieldExists = False
        for field in existingTableFields:
            if unicode(field["Field"]) == unicode(fieldToCheck):
                fieldExists = True
                break

        return fieldExists

    def checkTableFieldsExists(self, tableName="", fieldsToCheck=[]):
        fieldExistsCounter = 0
        for field in fieldsToCheck:
            if self.checkFieldExists(tableName=tableName, fieldToCheck=field):
                fieldExistsCounter += 1
        return True if fieldExistsCounter == len(fieldsToCheck) else False

    def checkTableExists(self, dbName=None, tableName=None):
        if dbName is None:
            dbName = self.dbName

        if not tableName:
            return False
        else:
            msql = "show tables"
            if dbName:
                msql += " from %s" % dbName

            r = list(x[0] for x in self.dbQuery(msql))
            if tableName in r:
                return True
            else:
                return False

    def dbMakeConnection(self):
        dbConnection = pymysql.connect(
            host=self.config["host"],
            user=self.config["user"],
            passwd=self.config["passwd"],
            db=self.config["db"],
            charset="utf8",
            use_unicode=True
        )
        self.systemName = "{host}_{db}".format(host=self.config["host"], db=self.config["db"])
        LOG.debug("SystemName: {sn}".format(sn=self.systemName))
        self.dbName = self.config["db"]
        dbConnection.autocommit = True
        return dbConnection

    def dbConnect(self):
        pass

    def dbClose(self):
        pass

    def dbGetConnection(self):
        connection = None

        while not connection:
            with self.dbLock:
                for con in self.dbConnections:
                    if con.acquire():
                        connection = con
                        break

                if not connection:
                    if len(self.dbConnections) < self.MAX_CONNECTIONS:
                        con = DatabaseConnection(self.dbMakeConnection, parent=self)
                        self.dbConnections.append(con)

        return connection

    def dbQuery(self, query, returnType=RETURN_LIST, callback=None, callbackStep=1, database=None, fetchResult=True,
                withMaxRows=False, byKey=None, cls=DbBareDataClass):
        dbConnection = self.dbGetConnection()
        ret = dbConnection.dbQuery(query, returnType, callback, callbackStep, database, fetchResult, withMaxRows, byKey, cls)
        dbConnection.release()
        # dbConnection.close()
        return ret

    def dbQueryDict(self, query, **argv):
        return self.dbQuery(query, returnType=self.RETURN_DICT, **argv)

    def dbQueryDictWithDB(self, query, database=None, **argv):
        return self.dbQueryDict(query, database=database, **argv)

    def dbQueryDictByKey(self, query, byKey, **argv):
        return self.dbQueryDict(query, byKey=byKey, **argv)

    def dbQueryWithoutResult(self, query, **argv):
        return self.dbQuery(query, fetchResult=False, **argv)

    def dbQueryWithMaxRows(self, query, **argv):
        return self.dbQuery(query, withMaxRows=True, **argv)

    def dbQueryObject(self, query, cls=DbBareDataClass, **argv):
        return self.dbQuery(query, returnType=self.RETURN_OBJECT, cls=cls, **argv)

    def dbQueryObjectByKey(self, query, byKey, cls=DbBareDataClass, **argv):
        return self.dbQueryObject(query, byKey=byKey, cls=cls, **argv)


class DatabaseConnectionWatcher(threading.Thread):
    def __init__(self, db=None):
        super(DatabaseConnectionWatcher, self).__init__()
        self.db = db
        self.daemon = True

    def run(self):
        while 1:

            for con in self.db.dbConnections:
                if con.acquire():
                    if con.expired():
                        con.close()
                    else:
                        con.release()

            count = len(self.db.dbConnections)
            # print "Open connections", count
            time.sleep(1)


class DatabaseProgrammingError(Exception):
    pass


class DatabaseConnection(object):
    timeOutDelta = datetime.timedelta(seconds=5)

    def __init__(self, makeConFunc, parent=None):
        self._lock = threading.Lock()
        self._makeConFunc = makeConFunc
        self._con = None
        self._parent = parent
        self._expires = None

    def updateExpires(self):
        self._expires = datetime.datetime.now() + self.timeOutDelta

    def expired(self):
        if self._expires:
            ret = self._expires < datetime.datetime.now()
        else:
            ret = False
        return ret

    def open(self):
        self._con = self._makeConFunc()
        self.updateExpires()

    def acquire(self, blocking=False):
        return self._lock.acquire(blocking)

    def release(self):
        return self._lock.release()

    def close(self):
        self._con.close()
        self._parent.dbConnections.remove(self)

    def cursor(self, cursorType=Database.LIST_CURSOR):
        return self._con.cursor(CustomDictCursor) if cursorType == Database.DICT_CURSOR else self._con.cursor()

    def dbQuery(self, *args, **kwargs):
        try:
            if not self._con:
                self.open()
            return self._dbQueryInner(*args, **kwargs)
        except pymysql.err.OperationalError as e:
            code, message = e.args
            if code in (2006, 2013):
                self.open()
                return self._dbQueryInner(*args, **kwargs)
            else:
                raise e

    def _dbQueryInner(self, query, returnType=Database.RETURN_LIST, callback=None, callbackStep=1, database=None, fetchResult=True,
                      withMaxRows=False, byKey=None, cls=DbBareDataClass):
        self.updateExpires()
        ret = []

        if withMaxRows:
            query = query.strip()
            spq = query.split()
            if spq[0].upper() == "SELECT":
                if spq[1].upper() != "SQL_CALC_FOUND_ROWS":
                    partlist = [spq[0], "SQL_CALC_FOUND_ROWS"]
                    partlist.extend(spq[1:])
                    query = " ".join(partlist)

        if returnType == Database.RETURN_LIST:
            cursor = self.cursor(Database.LIST_CURSOR)
        else:
            cursor = self.cursor(Database.DICT_CURSOR)

        if database:
            cursor.execute("use %s" % database)
        try:
            # if 1:
            affectedRows = cursor.execute(query)
        except pymysql.err.ProgrammingError as e:
            msg = "\nSQL:\n" + query + "\nPyMysql Error:\n" + str(e)
            raise DatabaseProgrammingError(msg)

        if byKey:
            ret = {}

        if fetchResult:
            if callback:

                row = cursor.fetchone()
                q = 0
                while row is not None:
                    q += 1
                    if q % callbackStep == 0:
                        callback(q, affectedRows)

                    obj = cls(dataDict=row) if returnType == Database.RETURN_OBJECT else None

                    if byKey:
                        ret[row[byKey]] = obj if returnType == Database.RETURN_OBJECT else row
                    else:
                        ret.append(obj if returnType == Database.RETURN_OBJECT else row)

                    row = cursor.fetchone()

            else:

                row = cursor.fetchone()
                while row is not None:
                    obj = cls(dataDict=row) if returnType == Database.RETURN_OBJECT else None

                    if byKey:
                        ret[row[byKey]] = obj if returnType == Database.RETURN_OBJECT else row
                    else:
                        ret.append(obj if returnType == Database.RETURN_OBJECT else row)

                    row = cursor.fetchone()

            if withMaxRows:
                cursor.execute("SELECT FOUND_ROWS() AS FOUNDROWS")
                if returnType == Database.RETURN_LIST:
                    maxRows = cursor.fetchone()[0]
                else:
                    maxRows = cursor.fetchone()["FOUNDROWS"]

                ret = (ret, maxRows)

        cursor.close()
        return ret
