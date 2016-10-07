import collections
from sortedcontainers import SortedListWithKey

from . import get_connection

class RedisBackend(object):
    """Descriptor for redis connection"""

    def __init__(self, db=None):
        self.db = db or get_connection()

    def __get__(self, instance, owner):
        return self.db


def sorted_list():
    return SortedListWithKey(key=lambda val: val[1])


class LocMemBackend(object):
    """Implements a redis-like interface on top of a dictionary of sorted lists"""

    def __init__(self):
        self._data = collections.defaultdict(sorted_list)

    def flushdb(self):
        self._data = collections.defaultdict(sorted_list)

    def zadd(self, key, members):
        self._data[key].update(members)

    def zrevrangebyscore(self, key, max, min, withscores=False):
        for index, (item, score) in enumerate(self._data):


    def zrange(self, key, start, stop, withscores=False):
        self._data[key]

    def zrevrange(self, key, start, stop, withscores=False):
        pass

    def zscore(self, key, elem):
        pass
