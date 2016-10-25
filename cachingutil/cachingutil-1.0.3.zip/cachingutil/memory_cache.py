# encoding: utf-8
"""
caching.py

Provides classes for in memory and file based caching
"""

import time
import requests
from abc import ABCMeta, abstractmethod
from base_cache import Cache

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


class BaseMemoryCache(Cache):

    __metaclass__ = ABCMeta  # Marks this as an abstract class

    EXPIRY_TIME = u'expiry time'
    CACHED_VALUE = u'cached value'

    @abstractmethod
    def calculate_expiry(self,
                         key):
        """
        RE-IMPLEMENT IN SUBCLASS IF MORE
        COMP

        :param key: key to retrieve the cached
        :return: expiry time integer epoch.
        """
        pass

    u"""
        ┌────────────────────────────┐
        │ Don't re-implement methods │
        │ below when subclassing...  │
        └────────────────────────────┘
     """

    def __init__(self,
                 auto_clear=True):
        """
        Cache items in memory. When expired, the item
        will be refetched, otherwise the cached item
        is used.

        :param auto_clear: each time the cache is accessed, expired items are
                           deleted.
        """
        super(BaseMemoryCache, self).__init__()
        self.__cache = {}
        self.__auto_clear = auto_clear

    def fetch_from_cache_by_key(self,
                                key):
        """
        Fetch an item in the cache.

        :param key: list of parameters required to
                       create a key into the cache
        :return: item from cache
        """
        return self.__cache[key][self.CACHED_VALUE]

    def expiry_time(self,
                    key):
        """
        Get the expiry time of the cached item.

        :return: expiry time as epoch seconds
        """
        try:
            return self.__cache[key][self.EXPIRY_TIME]
        except KeyError:
            return self.calculate_expiry(key)

    def clear_expired_items_from_cache(self):
        """
        Does what it says on the tin
        """
        delete_list = []
        for key in self.__cache:
            if self.expired(key=key):
                delete_list.append(key)

        for key in delete_list:
            self.delete_by_key(key)

    def pre_fetch_tasks(self,
                        **params):
        """
        Clears expired items from the cache
        :param params: not used in this case,
                       but required to swallow any
                       parameters supplied to by
                       the superclass.fetch
        :return: n/a
        """
        self.clear_expired_items_from_cache()

    def cache(self,
              item,
              **params):
        """
        Stores the item in the cache.
        The cached time is stored so that we can figure out
        when it has expired.

        :param item: item to cache
        :param params: list of parameters required to
                       fetch the item and create a key
        """
        key = self.key(**params)
        self.__cache[key] = {self.CACHED_VALUE: item}
        self.__cache[key][self.EXPIRY_TIME] = self.expiry_time(key)

    def delete_by_key(self,
                      key):
        """
        Deletes an item from the cache using its key

        :param key: key into cache
        """
        del self.__cache[key]


class SimpleMemoryCache(BaseMemoryCache):
    u"""
    Base class for caching objects in memory. This uses
    a common expiration for all objects (

    When subclassing, the 'key' and 'fetch_from_source'
    methods should be written.

    'key' should return a unique key.

    'fetch_from_source needs to returns a requests
    response.
    """
    __metaclass__ = ABCMeta  # Marks this as an abstract class

    u"""
        ┌────────────────────────────┐
        │ Don't re-implement methods │
        │ below when subclassing...  │
        └────────────────────────────┘
     """

    def __init__(self,
                 max_age,
                 auto_clear=True):
        """
        Cache items in memory. When expired, the item
        will be refetched, otherwise the cached item
        is used.

        :param auto_clear: each time the cache is accessed, expired items are
                           deleted.
        """
        super(SimpleMemoryCache, self).__init__(auto_clear=auto_clear)
        self.__max_age = max_age

    def calculate_expiry(self,
                         key):
        """
        RE-IMPLEMENT IN SUBCLASS IF MORE
        COMP

        :param key: key to retrieve the cached
        :return: expiry time integer epoch.
        """
        return time.time() + self.__max_age


class BaseHttpMemoryCache(BaseMemoryCache):

    u"""
    Base class for caching HTTP requests in memory.

    When subclassing, the 'key' and 'fetch_from_source'
    methods should be written.

    If caching objects generated from the request,
    then also write get_request_for_item, which should
    pull the request from the object

    'key' should return a unique key. If this is just
    the URL, you can use the HttpMemoryCache class
    below.

    'fetch_from_source needs to returns a requests
    response.
    """
    __metaclass__ = ABCMeta  # Marks this as an abstract class

    @staticmethod
    def max_age(request):
        try:
            max_age = [cc.split(u'=')[1] for cc in request.headers[u'cache-control'].split(u',') if u'max-age' in cc][0]
            return int(time.time()) + int(max_age)
        except KeyError:
            return 0
        except IndexError:
            return 0

    def get_request_for_item(self,
                             item):
        """
        :param item: cached item
        :return: request component of item
        """
        return item

    def calculate_expiry(self,
                         key):
        request = self.get_request_for_item(self.fetch_from_cache_by_key(key))

        return self.max_age(request)


class HttpMemoryCache(BaseHttpMemoryCache):
    """
    Concrete class for caching general HTTP requests in memory.
    """
    def key(self,
            url,
            **params):
        return url

    def fetch_from_source(self,
                          url,
                          **params):
        return requests.get(url)
