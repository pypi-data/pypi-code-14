#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import codecs

import six


def stringify(value):
    """
    Take element and get a string representation of it. Works for nested elements like lists, tuples and dicts.
    Will alphanumerically order dicts. Useful for hashing primitives.

    :rtype: str
    """
    if isinstance(value, six.text_type):
        return codecs.encode(value.encode(), "hex").decode()

    elif isinstance(value, six.binary_type):
        return codecs.encode(value, "hex").decode()

    elif isinstance(value, int):
        return hex(value)

    elif isinstance(value, (list, tuple)):
        return "[%s]" % ",".join(map(stringify, value))

    elif isinstance(value, dict):
        items = [(key, value[key]) for key in sorted(value.keys())]
        return "{%s}" % ",".join(map(lambda p: "%s:%s" % (stringify(p[0]), stringify(p[1])), items))

    elif value is None:
        return "!"

    else:
        raise TypeError("Unknown type: %s" % (type(value),))
