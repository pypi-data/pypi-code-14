# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from marshmallow import Schema as BaseSchema, validate
from marshmallow.fields import Integer, Boolean, String, Raw, Nested, List

ALLOWED_OPS = [
    '==',
    '!=',
    '>',
    '>=',
    '<',
    '<=',
    'range',  # between start (value[0]) and end (value[1])
    'in',  # one of
    '~in',  # not one of
    '^',  # starts with
    '~^',  # not starts with
    'has',  # contains
    '~has',  # not contains
    '$',  # ends with
    '~$',  # not ends with
]


# sync with pump/pump/apischema.py


class MetricSchema(BaseSchema):
    field = String(required=True, validate=[validate.Length(min=1)])
    aggregation = String()
    alias = String()


class FilterSchema(BaseSchema):
    field = String(required=True, validate=[validate.Length(min=1)])
    operator = String(validate=[validate.OneOf(ALLOWED_OPS)])
    value = Raw(required=True)
    type = String()  # 用于类型转换


class QuerySchema(BaseSchema):
    ds_type = String(required=True)
    ds_dsn = String(required=True)
    table = String(required=True)
    metrics = Nested(MetricSchema, many=True)
    filters = Nested(FilterSchema, many=True)
    groupby = List(String(), default=[], missing=[])
    orderby = List(String(), default=[], missing=[])
    limit = Integer()
    q = String(default='', missing='')
    cache_timeout = Integer(default=0, missing=0)
    force = Boolean(default=False, missing=False)


query_schema = QuerySchema()
