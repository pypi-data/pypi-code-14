# encoding: utf-8
from commons.persistence import get_all


def fromSchema(f):
    def underlaying(schema):
        data, errors = schema
        if errors:
            raise RuntimeError(errors)

        f.__globals__['schema'] = schema

        return f(data)

    underlaying.__name__ = f.__name__
    underlaying.__doc__ = f.__doc__

    return underlaying


def filter_all(model, **kwargs):
    return (dict(i) for i in get_all(model, *zip(*kwargs.items())))


def query_all(model):
    return (dict(i) for i in get_all(model))
