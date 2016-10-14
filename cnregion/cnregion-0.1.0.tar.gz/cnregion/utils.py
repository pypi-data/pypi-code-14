# coding: utf-8

from itertools import tee

try:
    from itertools import izip
except ImportError:
    izip = zip


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def bisect_search_left(a, x, key, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)

    while lo < hi:
        mid = (lo+hi) // 2
        if key(a[mid]) < x:
            lo = mid+1
        else:
            hi = mid
    return lo


def bisect_search(a, x, key, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)

    while lo < hi:
        mid = (lo+hi) // 2
        if x < key(a[mid]):
            hi = mid
        else:
            lo = mid+1
    return lo


bisect_search_right = bisect_search


class cached_property(object):

    def __init__(self, func):
        self.func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def normalize_name(name):
    items = name.split()
    length = len(items)

    if length >= 3 and items[1] in (u'北京', u'上海', u'重庆', u'天津', u'北京市', u'上海市', u'重庆市', u'天津市') and items[2] not in (u'县', u'市辖区'):
        if items[2].endswith(u'县'):
            items.insert(2, u'县')
        else:
            items.insert(2, u'市辖区')
        return ' '.join(items)

    return name
