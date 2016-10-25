# encoding: utf-8
"""
caching.py

Provides classess for in memory and file based caching
"""

import os
import sys
import codecs
from abc import ABCMeta, abstractmethod
from base_cache import Cache, CacheError
from binary_file_cache import BinaryFileCache

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


class FileCache(BinaryFileCache):

    __metaclass__ = ABCMeta  # Marks this as an abstract class

    # Also re-implement filename, fetch_from_source from BinaryFileCache

    @staticmethod
    def encode(data):
        """
        Converts the data into a writable form.

        Re-implement if serialisation is required. (e.g. using pickle)

        :param data: data/object to serialise
        :return: serialised data
        """
        encoded = data
        return encoded

    @staticmethod
    def decode(encoded):
        """
        Converts the raw data read into a usable form.

        Re-implement if serialisation is required. (e.g. using pickle)

        :param encoded: seriealise data to deserialise
        :return: deserialised data
        """
        decoded = encoded
        return decoded

    u"""
        ┌────────────────────────────┐
        │ Don't re-implement methods │
        │ below when subclassing...  │
        └────────────────────────────┘
     """

    def __init__(self,
                 max_age=0,
                 folder=None,
                 encoding=u'UTF-8'):
        """
        Cached data to files. When the are older than max_age, the date
        will be refetched. When younger than max_age, the cached file
        is used.

        Note that old cached files are not automatically deleted, but
        will be replaces when a new fetch is made.

        :param max_age: time in seconds to maintain the cached files
                        the default is 0, which is to never expire.
        :param folder: path to the folder intended to contain the cached files
        """
        super(FileCache, self).__init__(max_age=max_age,
                                        folder=folder)
        self.encoding = encoding

    def cache(self,
              item,
              **params):
        """
        Writes the data in 'value' to the cached file

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param item: data to write to the cache
        :param params: parameters required to build the filename
        :return: n/a
        """
        # TODO write to a temporary file and move
        with codecs.open(filename=self.key(**params),
                         encoding=self.encoding,
                         mode=u'w') as cached_file:
            cached_file.write(unicode(self.encode(item)))

    def fetch_from_cache_by_key(self,
                                key):
        """
        Returns the contents of the cached file

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param key: key required to build the filename
        :return: contents of the cached file
        """
        with codecs.open(filename=key,
                         encoding=self.encoding,
                         mode=u'r') as cached_file:
            return self.decode(cached_file.read())

