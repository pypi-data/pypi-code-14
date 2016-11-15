# -*- coding: utf-8 -*-
from threading import Thread

import psycopg2

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

import pickle
import StringIO
import hashlib


class DatabaseConnection(object):
    """
        This class connects to specified database for data retrieval and caching.
    """

    def __init__(self, table_name, database, user, password, host):
        self.table_name = table_name
        self.local_cache = {}

        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS %s (id TEXT NOT NULL PRIMARY KEY, data BYTEA NOT NULL);" % self.table_name)
        self.conn.commit()

    def __insert_row(self, row_id, data):
        sql = "INSERT INTO " + self.table_name + " (id, data) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data;"
        parameters = (row_id, psycopg2.Binary(pickle.dumps(data)),)
        self.cursor.execute(sql, parameters)
        self.conn.commit()

    def fetch_result_from_db(self, row_id):
        """

        :param row_id:
        :return:
        """
        sql = "SELECT data FROM " + self.table_name + " WHERE id = %s"
        parameters = (row_id,)
        self.cursor.execute(sql, parameters)
        cached = self.cursor.fetchone()
        if cached:
            return pickle.load(StringIO.StringIO(cached[0]))
        else:
            return False

    def cache_result_to_db(self, row_id, data):
        """

        :param row_id:
        :param data:
        :return:
        """
        insert_thread = Thread(target=self.__insert_row, args=(row_id, data,), name="Network Database Insertion")
        insert_thread.start()
        return insert_thread


class Cache(object):
    """
        This class create decorators to cache function return value in database, and retrieve them when possible.
    """

    def __init__(self, database="test", user="benjamin", password="", host="db.bchiang.cc"):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.compute_methods = {'async': self.async_compute, 'sync': self.sync_compute}

    @staticmethod
    def async_compute(db_connection, row_id, local_func):
        """

        :param db_connection:
        :param row_id:
        :param local_func:
        :return:
        """
        que = Queue()

        def __loc():
            ret = local_func()
            db_connection.cache_result_to_db(row_id, ret)
            que.put(ret)

        def __net():
            ret = db_connection.fetch_result_from_db(row_id)
            if ret:
                que.put(ret)

        local_thread = Thread(target=__loc, name='Execute Wrapped Function')
        network_thread = Thread(target=__net, name='Network Database Retrieval')
        network_thread.start()
        local_thread.start()

        return que.get()

    @staticmethod
    def sync_compute(db_connection, row_id, local_func):
        """

        :param db_connection:
        :param row_id:
        :param local_func:
        :return:
        """
        net_ret = db_connection.fetch_result_from_db(row_id)
        if net_ret:
            return net_ret
        else:
            loc_ret = local_func()
            db_connection.cache_result_to_db(row_id, loc_ret)
            return loc_ret

    def use_table(self, table_name, mode='sync'):
        """

        :param table_name: The table used in the database
        :return: Return value of the decorated function
        """

        db_connection = DatabaseConnection(table_name=table_name, database=self.database, user=self.user,
                                           password=self.password, host=self.host)

        def __decorator(func):
            def __wrapper(*args, **kw):
                pickle_row_id = pickle.dumps((func.__name__, args, kw))
                row_id = hashlib.sha224(pickle_row_id).hexdigest()

                def __wrapped_executable_function():
                    return func(*args, **kw)

                return self.compute_methods.get(mode)(db_connection, row_id, __wrapped_executable_function)

            return __wrapper

        return __decorator
