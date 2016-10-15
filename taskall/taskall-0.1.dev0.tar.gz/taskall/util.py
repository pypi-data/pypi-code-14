__author__ = 'shadyrafehi'

import base64
import time

try:
    import dill
    _serializer = dill
except ImportError:
    import pickle
    _serializer = pickle


def deserialize(string):
    return _serializer.loads(base64.b64decode(string))


def serialize(obj):
    return base64.b64encode(_serializer.dumps(obj))


def timer(func):
    import functools

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        name = func.__name__
        print 'Function `{}`: timing now...'.format(name)
        t0 = time.time()
        result = func(*args, **kwargs)
        t = time.time() - t0
        print 'Function `{}`: executed in {:0.2f} seconds'.format(name, t)
        return result

    return wrap
