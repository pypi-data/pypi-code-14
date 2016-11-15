# -*- coding: utf-8 -*-
import warnings

import psycopg2


class Cache(object):
    def __init__(self, database="test", user="benjamin", password="", host="db.bchiang.cc"):
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host)
        self.cursor = self.conn.cursor()

    def create_table(self, name):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS %s (id TEXT NOT NULL, data TEXT NOT NULL);" % name)
        self.conn.commit()

    def insert_row(self, table_name, row_id, data):
        sql = "INSERT INTO " + table_name + " (id, data) VALUES (%s, %s);"
        parameters = (row_id, data,)
        self.cursor.execute(sql, parameters)
        self.conn.commit()

    def fetch_data(self, table_name, row_id):
        sql = "SELECT data FROM " + table_name + " WHERE id = %s"
        parameters = (row_id,)
        self.cursor.execute(sql, parameters)
        cached = self.cursor.fetchone()
        if cached:
            return cached[0]
        else:
            return False

    def create_function_decorator(self, table_name):
        self.create_table(table_name)

        def decorator(func):
            def wrapper(*args, **kw):
                arg_str = "-".join([str(a) for a in args])
                row_id = "%s-%s" % (func.__name__, arg_str)

                cached_data = self.fetch_data(table_name, row_id)
                if not cached_data:
                    cached_data = func(*args, **kw)
                    if cached_data is not None:
                        self.insert_row(table_name, row_id, cached_data)
                    else:
                        warnings.warn("Decorated function returned null. Nothing to Cache")
                return cached_data

            return wrapper

        return decorator
