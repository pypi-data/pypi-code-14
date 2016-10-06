# encoding: utf-8
"""
caching.py

Provides classess for in memory and file based caching
"""

import time
from abc import ABCMeta, abstractmethod

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


class CacheError(Exception):
    pass


class Cache(object):

    __metaclass__ = ABCMeta  # Marks this as an abstract class

    def __init__(self):
        """
        Subclass this to fetch and cache items with provision
        for expiration rules.
        """
        pass

    @abstractmethod
    def key(self,
            **params):
        """
        Create a key into the cache

        :param params: list of parameters require to
                       create a key into the cache
        :return: key into the cache
        """
        pass

    @abstractmethod
    def fetch_from_source(self,
                          **params):
        """
        Fetch an uncached item.

        :param params: list of parameters required to
                       fetch the item and create a key
        :return: item to cache and return
        """
        pass

    @abstractmethod
    def cache(self,
              item,
              **params):
        """
        Store an item in the cache.

        :param item: item to be cached
        :param params: list of parameters required to
                       create a key into the cache
        :return: key into the cache
        """
        pass

    @abstractmethod
    def fetch_from_cache_by_key(self,
                                key):
        """
        Fetch the item from the cache by key

        :param key: key into cache
        :return:
        """
        pass

    @abstractmethod
    def delete_by_key(self,
                      key):
        """
        Delete an item from the cache.

        :param key: list of parameters required to
                    fetch the item and create a key
        """
        pass

    def delete(self,
               **params):
        """
        Delete an item from the cache.

        :param params: list of parameters required to
                       fetch the item and create a key
        """
        self.delete_by_key(self.key(**params))

    def clear_expired_items_from_cache(self):
        """
        Implement in subclass if required
        """
        pass

    def cached_time(self,
                    key):
        """
        Get the global expiry time.

        Implement in subclass this if expiry_time
        can't be directly determined.

        :return: time in seconds when items older
                 than this should be deemed to have
                 expired
        """
        pass

    @abstractmethod
    def expiry_time(self,
                    key):
        """
        Get the expiry time of the item.

        :return: time in seconds when items older
                 than this should be deemed to have
                 expired
        """
        pass

    def _fetch_from_cache(self,
                          **params):
        """
        Fetch an item in the cache.

        :param params: list of parameters required to
                       create a key into the cache
        :return: item from cache
        """
        try:
            return self.fetch_from_cache_by_key(key=self.key(**params))
        except KeyError:
            raise CacheError()

    def pre_fetch_tasks(self,
                        **params):
        """
        Optional to implement in subclass.
        An example use is to clear expired items from the cache.

        :param params:
        :return: n/a
        """
        pass

    def expired(self,
                key = None,
                **params):
        """
        Returns a flag to indicate if the item in the cache
        for the given key has expired.

        DO NOT RE-IMPLEMENT IN SUBCLASS

        :param key: key to the item in the cache
               **params: alternative to allow for checking outside
                         the caching class without needing the key.
        :return: bool: True if the item has expired from the cache
        """
        key = (key
               if key is not None
               else self.key(**params))
        try:
            return self.expiry_time(key) <= time.time()
        except KeyError as ke:
            raise CacheError(ke)

    def fetch(self,
              **params):
        """
        IF an item is not in the cache or has expired, it is
        fetched from source and cached.
        If it in the cache an not expired, it's fetched from
        the cache and returned.

        DO NOT RE-IMPLEMENT IN SUBCLASS

        :param params: parameters required to generate a unique key
                       into the cache and to fetch uncached items
        :return: cached or uncached item.
        """
        self.pre_fetch_tasks(**params)

        try:
            if not self.expired(**params):
                return self._fetch_from_cache(**params)
        except CacheError:
            pass

        cached_value = self.fetch_from_source(**params)

        self.cache(item=cached_value,
                   **params)

        return cached_value
