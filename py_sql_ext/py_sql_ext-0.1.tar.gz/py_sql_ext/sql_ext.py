# -*- coding:UTF-8 -*-


from sqlalchemy.sql import text
import logging
import transaction

__author__ = 'peng'

'''
sql扩展,查询返回的结果是dict
'''

"""
可加入判断的sql语句
"""

debug_mode = False


def init_engine(engine, debug=False):
    transaction.init_engine(engine)
    debug_mode = False


_template_cache = dict()


def _render_sql(sql_template, **kwargs):
    if '{{' in sql_template:

        from jinja2 import Template
        cache_key = "template_" + sql_template
        if cache_key in _template_cache:
            template = _template_cache[cache_key]
        else:
            template = Template(sql_template)
            _template_cache[cache_key] = template
        sql = template.render(**kwargs)
    else:
        sql = sql_template
    return sql


def _execute_sql(sql, **kwargs):
    if debug_mode:
        log_str = u"执行SQL:%s \n 参数: %s" % (sql, kwargs)
    result = transaction.get_session().execute(text(sql), params=dict(**kwargs))
    if debug_mode:
        logging.debug(u'%s\n 结果: 受影响行数:%d id:%s' % (log_str, result.rowcount, result.lastrowid))
    return result


def _close_result(result):
    result.close()


def query_all_template(sql_template, sql_template_real=None):
    function_doc = None
    if sql_template_real:
        function_doc = sql_template
        sql_template = sql_template_real

    def wrap_query(**kwargs):
        sql = _render_sql(sql_template, **kwargs)
        result = _execute_sql(sql, **kwargs)
        data = [dict(zip(i.keys(), i.values())) for i in result]
        _close_result(result)
        return data

    wrap_query.__doc__ = function_doc
    return wrap_query


def query_one_template(sql_template, sql_template_real=None):
    function_doc = None
    if sql_template_real:
        function_doc = sql_template
        sql_template = sql_template_real

    def wrap_query(**kwargs):
        sql = _render_sql(sql_template, **kwargs)
        result = _execute_sql(sql, **kwargs)
        row = None
        # 获取第一行数据
        for i in result:
            row = dict(zip(i.keys(), i.values()))
            break
        _close_result(result)
        return row

    wrap_query.__doc__ = function_doc
    return wrap_query


def query_scalar_list_template(sql_template, sql_template_real=None):
    function_doc = None
    if sql_template_real:
        function_doc = sql_template
        sql_template = sql_template_real

    def wrap_query(**kwargs):
        sql = _render_sql(sql_template, **kwargs)
        result = _execute_sql(sql, **kwargs)
        data = [i.values()[0] for i in result]
        _close_result(result)
        return data

    wrap_query.__doc__ = function_doc
    return wrap_query


def query_scalar_template(sql_template, sql_template_real=None):
    function_doc = None
    if sql_template_real:
        function_doc = sql_template
        sql_template = sql_template_real

    def wrap_query(**kwargs):
        sql = _render_sql(sql_template, **kwargs)
        result = _execute_sql(sql, **kwargs)
        scalar = result.scalar()
        _close_result(result)
        return scalar

    wrap_query.__doc__ = function_doc
    return wrap_query


def add_template(sql_template, sql_template_real=None):
    function_doc = None
    if sql_template_real:
        function_doc = sql_template
        sql_template = sql_template_real

    def wrap_query(**kwargs):
        sql = _render_sql(sql_template, **kwargs)
        result = _execute_sql(sql, **kwargs)
        last_row_id = result.lastrowid
        _close_result(result)
        return last_row_id

    wrap_query.__doc__ = function_doc
    return wrap_query


def update_template(sql_template, sql_template_real=None):
    function_doc = None
    if sql_template_real:
        function_doc = sql_template
        sql_template = sql_template_real

    def wrap_query(**kwargs):
        sql = _render_sql(sql_template, **kwargs)
        result = _execute_sql(sql, **kwargs)
        row_count = result.rowcount
        _close_result(result)
        return row_count

    wrap_query.__doc__ = function_doc
    return wrap_query


def delete_template(sql_template, sql_template_real=None):
    function_doc = None
    if sql_template_real:
        function_doc = sql_template
        sql_template = sql_template_real

    def wrap_query(**kwargs):
        sql = _render_sql(sql_template, **kwargs)
        result = _execute_sql(sql, **kwargs)
        row_count = result.rowcount
        _close_result(result)
        return row_count

    wrap_query.__doc__ = function_doc
    return wrap_query
