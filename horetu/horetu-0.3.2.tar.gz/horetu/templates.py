import os
from abc import ABCMeta
from functools import wraps, partial

def AppIter(x):
    '''
    :param x: Anything (returned from the underlying program)
    :rtype: Iterable of bytes
    :returns: Output as bytes
    '''
    if x is None:
        raise StopIteration
    elif isinstance(x, bytes):
        yield x
    elif isinstance(x, str):
        yield x.encode('utf-8')
    elif hasattr(x, '__iter__'):
        for y in x:
            yield from AppIter(y)
    else:
        yield format(x).encode('utf-8')
