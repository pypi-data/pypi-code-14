# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Various utils
"""
import sys

from functools import WRAPPER_ASSIGNMENTS

PYTHON_VERSION = sys.version_info[0]

if PYTHON_VERSION == 2:
    STRING_CLASS = basestring
    UNICODE_CLASS = unicode
elif PYTHON_VERSION == 3:
    STRING_CLASS = str
    UNICODE_CLASS = str


def is_string(value):
    """ Check if a value is a valid string, compatible with python 2 and python 3

    >>> is_string('foo')
    True
    >>> is_string(u'✌')
    True
    >>> is_string(42)
    False
    >>> is_string(('abc',))
    False
    """
    return isinstance(value, STRING_CLASS)


def is_unicode(value):
    """ Check if a value is a valid unicode string, compatible with python 2 and python 3

    >>> is_unicode(u'foo')
    True
    >>> is_unicode(u'✌')
    True
    >>> is_unicode(b'foo')
    False
    >>> is_unicode(42)
    False
    >>> is_unicode(('abc',))
    False
    """
    return isinstance(value, UNICODE_CLASS)


def to_latin_1(value):
    """ Return the input string encoded in latin1 with replace mode for errors
    """
    return value.encode('latin-1', 'replace')


def update_wrapper(wrapper, wrapped):
    """ Update wrapper attribute to make it look like wrapped function.
    Don't use original update_wrapper because it can breaks if wrapped don't
    have all attributes.
    """
    for attr in WRAPPER_ASSIGNMENTS:
        if hasattr(wrapped, attr):
            setattr(wrapper, attr, getattr(wrapped, attr))
    return wrapper
