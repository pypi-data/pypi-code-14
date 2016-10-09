"""Utility functions for RingPlus."""

from __future__ import print_function

import six


def convert_to_utf8_str(arg):
    # written by Michael Norton (http://docondev.blogspot.com
    if isinstance(arg, six.text_type):
        arg = arg.encode('utf-8')
    elif not isinstance(arg, bytes):
        arg = six.text_type(arg).encode('utf-8')
    return arg


def import_simplejson():
    try:
        import simplejson as json
    except ImportError:
        try:
            import json  # Python 2.6+
        except:
            try:
                # Google App Engine
                from django.utils import simplejson as json
            except ImportError:
                raise ImportError("Can't load a json library.")

    return json
