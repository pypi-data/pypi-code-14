#!/usr/bin/python
# -*- coding:utf-8 -*-
#####################################
# Author: heshihui
# Date: 2016-08-16
# Desc:
# This module includes two classes below.
# An instance of the `CommandResult` class
# may be looked as a DTO(Data Transfer Object).Some of methods in the `PipelineDBClicent`
# class return result that is an instance of the `CommandResult` class.
# You can use straight the object of `PipelineDBClicent` class to operate hive.
######################################

import os
import sys  
import subprocess
import re
import logging
import psycopg2


_logger = logging.getLogger(__name__)


class PipelineDBClient(object): 
    """PipelineDBClicent may be looked as a wrapper of pipelinedb.

    You can create an object of PipelineDBClicent,then execute most of pipelinedb sql
    by the class methods.


    Raises
    ------
    Error
        the database connection has error.
   
    Examples
    --------
    >>> import client
    >>> pipeline = client.PipelineDBClient()
    >>> sql = 'select * from testhhh limit 10'
    >>> pipeline.query(sql)
    >>> for row in pipeline.fetch(sql=sql,maxRowCount=5):
    ...       print row
    ...
   
    (2, '20160816', '2', 698906L)
    (3, '20160816', '3', 66890098L)
    (4, '20160816', '4', 5376L)
    (5, '20160816', '5', 2467L)
    (6, '20160816', '1', 89999L)

    """



    def __init__(self):
        try:
            self._conn = psycopg2.connect('dbname=pipeline user=pipeline host=192.168.223.154 port=5888')
        except Exception,e:
            print e
            _logger.error("the database connection has error is %s" % (e))
        self._cur = self._conn.cursor()


    def query(self,sql):
        try:
            result = self._cur.execute(sql)
        except Exception,e:
            print e
            _logger.error("数据查询出错：%s" % (e))
            result = False
        return result

    #返回结果列表
    def fetchAllRows(self):
        return self._cur.fetchall()

    def fetchOneRows(self):
        return self._cur.fetchone()

    def fetch(self, vars=None, sql=None, sql_file=None,  maxRowCount=-1, vars_pattern="${var:#value}"):
         # validate the parameters
        if vars and not isinstance(vars, dict):
            raise ValueError(
                "the function sql:The argument variable_substitution must be dict type.")

        if sql_file is None and sql is None:
            raise ValueError(
                "the function sql:At least one argument of sql_file and sql passed.")

        if sql_file and not os.path.exists(sql_file):
            raise ValueError(
                "The hive sql file:%s doesn't exists." % (sql_file))

        if sql_file:
            with open(sql_file, "r") as file:
                lines = file.readlines()
            sql = "".join(lines)

        if vars:
            for element in vars.items():
                var_key = vars_pattern.replace("#value", element[0])
                sql = sql.replace(var_key, element[1])

        _logger.info("fetch sql:%s" % (sql))
        count = 0
        self._cur.execute(sql)
        for row in self._cur:
            yield row
            count += 1
            if maxRowCount>=0 and count>=maxRowCount:
                break

        return

    # commit
    def commit(self):
        self._conn.commit()

    def __del__(self):
        try:
            self._cur.close() 
            self._conn.close() 
        except:
            pass
            
    #关闭数据库
    def close(self):
        self.__del__()


    #显示所有数据库，返回一个列表
    def show_databases(self):

        sql = "select * from pg_database"
        _logger.debug("show databases sql is :%s" % (sql))
        self.query(sql)
        rs = self.fetchAllRows()
        databases = []
        for element in rs:
            databases.append(element[0])
        return databases


    def show_tables(self):

        sql = "select tablename from pg_catalog.pg_tables where schemaname='public'"
        _logger.debug("show tables sql is:%s" % (sql))
        self.query(sql)
        rs = self.fetchAllRows()
        tables = []
        for element in rs:
            tables.append(element[0])
        return tables


    def has_table(self, table_name):
        tables = self.show_tables()
        for table in tables:
            if table == table_name:
                return True
        return False


    def show_views(self):

        sql = "select viewname from pg_catalog.pg_views where schemaname='public'"
        _logger.debug("show views sql is:%s" % (sql))
        self.query(sql)
        rs = self.fetchAllRows()
        views = []
        for element in rs:
            views.append(element[0])
        return views



    def desc_table(self,table_name):
        "returns a dict of columns"

        if not table_name:
            raise ValueError(
                "this table_name value shouldn't be empty string.")

        self.query( "select column_name,data_type from information_schema.columns where table_schema = 'public' and table_name = '%s'" %(table_name))
        rs = self.fetchAllRows()
        table_info = {"fields": []}
        for element in rs:
            column_info = {}
            column_info['name'] = element[0]
            column_info['type'] = element[1]
            table_info['fields'].append(column_info)

        return table_info


    def drop_table(self, table_type, table_name):
        pipelinedb_sql = 'drop %s %s' % (table_type, table_name)
        _logger.debug("executed pipelinedb sql:%s" % (pipelinedb_sql))
        self._cur.execute(pipelinedb_sql)
        self.commit()
        self.close()

    



    def execute(self, sql, seq_of_parameters=None):
        """this method can be used to execute pipelinedb sql.

        Parameters
        ----------
        sql : str
            The pipelinedb sql,if this parameter is required.
        seq_of_parameters : str
            The parameter is a list of tuple.

        """
        _logger.debug("execute sql:%s,parameters:%s" % (sql,seq_of_parameters))
        self._cur.executemany(sql,seq_of_parameters)
        self.commit()
        return self._cur.rowcount
