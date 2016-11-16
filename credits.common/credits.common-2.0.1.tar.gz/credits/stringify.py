#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools


@functools.singledispatch
def as_string(obj):
    raise TypeError("Unknown type: %s." % (type(obj, )))


@as_string.register(bytes)  # noqa
def _(obj: bytes):
    return obj.hex()


@as_string.register(str)  # noqa
def _(obj: str):
    return obj.encode().hex()


@as_string.register(int)  # noqa
def _(obj: int):
    return hex(obj)


@as_string.register(dict)  # noqa
def _(obj: dict):
    return "{" + ",".join(("%s:%s" % (as_string(k), as_string(v))) for (k, v) in sorted(obj.items())) + "}"


@as_string.register(tuple)  # noqa
@as_string.register(list)  # noqa
def _(value: list):
    return "[" + ",".join(map(as_string, value)) + "]"


@as_string.register(type(None))  # noqa
def _(value: type(None)):
    return "!"
