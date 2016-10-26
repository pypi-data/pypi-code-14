# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from dateutil.parser import parse as dateparse

from .compat import string_types


def map_udf(udf):
    return {
        'day': 'day',
        'daily': 'day',
        'week': 'week',
        'weekly': 'week',
        'month': 'month',
        'monthly': 'month',
        'year': 'year',
        'yearly': 'year'
    }.get(udf, udf)


def map_order_dir(direction):
    return {
        '+': '+',
        '-': '-',
        'asc': '+',
        'desc': '-'
    }[direction]


def check_string_type(value):
    if not isinstance(value, string_types):
        raise ValueError('value must be string type')


def ensure_list(v):
    if isinstance(v, (list, set, tuple)):
        return list(v)
    return v is not None and [v] or []


def cast(value, typ):
    if isinstance(typ, type):
        typ = typ.__name__.lower()
    elif isinstance(typ, string_types):
        typ = typ.lower()
    else:
        typ = type(typ).__name__.lower()

    if typ in ['int', 'int32', 'int64', 'long', 'integer', 'bigint', 'smallint', 'tinyint', 'short']:
        return int(value)
    if typ in ['float', 'double', 'numeric', 'number', 'decimal', 'number(real)']:
        return float(value)
    if typ in [x for x in string_types] + ['varchar', 'string', 'char', 'text']:
        return str(value)
    if typ in ['datetime', 'timestamp']:
        return dateparse(value).strftime('%Y-%m-%d %H:%M:%S')
    if typ in ['date']:
        return dateparse(value).strftime('%Y-%m-%d')
    return value


def extract_func_field(s):
    """Extract function name (if exists) and field name"""
    x = re.match('([a-z]+)\((.+)\)', s)
    if x is not None:
        func, field = x.groups()
    else:
        func, field = None, s
    return func, field


def make_alias(func, field):
    return '{}__{}'.format(func, field)


def get_col_name(metric_or_groupby):
    """根据 Pump 的规则, 计算结果集中的列名。

    :param metric_or_groupby: metric (dict) 或 groupby 的字段(string 或 tuple)
    :return: 列名
    :rtype: basestring

    >>> metric = {'field': 'id', 'aggregation': 'max', 'alias': 'max_id'}
    >>> get_col_name(metric)
    max_id

    >>> metric = {'field': 'id', 'aggregation': 'max', 'alias': ''}
    >>> get_col_name(metric)
    max__id

    >>> metric = {'field': 'id', 'aggregation': 'max'}
    >>> get_col_name(metric)
    max__id

    >>> groupby = 'daily(created_at)'
    >>> get_col_name(groupby)
    day__created_at

    >>> groupby = 'day(created_at)'
    >>> get_col_name(groupby)
    day__created_at

    >>> groupby = ('created_at', 'weekly')
    >>> get_col_name(groupby)
    week__created_at
    """
    if isinstance(metric_or_groupby, string_types):
        udf, field = extract_func_field(metric_or_groupby)
        if udf:
            return make_alias(map_udf(udf), field)
        return field
    elif isinstance(metric_or_groupby, tuple):
        # metric: (field, aggregation)
        # groupby: (field, udf)
        field, func = metric_or_groupby[:2]
        return make_alias(map_udf(func), field)
    elif isinstance(metric_or_groupby, dict):
        # metric: {"field": field, "aggregation": agg, "alias": alias}
        if metric_or_groupby.get('alias'):
            return metric_or_groupby['alias']
        agg = metric_or_groupby.get('aggregation')
        if agg:
            return make_alias(agg, metric_or_groupby['field'])
        return metric_or_groupby['field']
