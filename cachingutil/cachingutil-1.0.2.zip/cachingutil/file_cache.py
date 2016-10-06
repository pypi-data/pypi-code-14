# encoding: utf-8
"""
caching.py

Provides classess for in memory and file based caching
"""

import os
import codecs
from abc import ABCMeta, abstractmethod
from base_cache import Cache, CacheError

__author__ = u'Hywel Thomas'
__copyright__ = u'Copyright (C) 2016 Hywel Thomas'


class FileCache(Cache):

    __metaclass__ = ABCMeta  # Marks this as an abstract class

    # Also re-implement

    @abstractmethod
    def filename(self,
                 **params):
        """
        Generates a filename for the cached file.

        :param params: parameters required to build the filename
        :return: filename with extension, without path
        """
        raise NotImplementedError(u'FileCache.filename must be implemented')

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
                 max_age,
                 folder=None):
        """
        Cached data to files. When the are older than max_age, the date
        will be refetched. When younger than max_age, the cached file
        is used.

        Note that old cached files are not automatically deleted, but
        will be replaces when a new fetch is made.

        :param max_age: time in seconds to maintain the cached files
        :param folder: path to the folder intended to contain the cached files
        """
        super(Cache, self).__init__()
        self.__max_age = max_age
        self.__folder = folder
        if os.path.exists(folder):
            if not os.path.isdir(folder):
                raise CacheError(u'Invalid folder:"{folder}"'.format(folder=folder))
        else:
            try:
                os.makedirs(folder)
            except Exception as e:
                raise CacheError(u'Could not create folder:"{folder}" because:"{e}"'
                                 .format(folder=folder,
                                         e=e))

    def key(self,
            **params):
        """
        Assembles folder path and filename

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param params: parameters required to build the filename
        :return: full path to the file
        """
        return os.path.normpath(os.path.join(self.__folder, self.filename(**params)))

    def expiry_time(self,
                    key):
        """
        Get the expiry time of the item.

        :return: expiry time as epoch seconds
        """
        if os.path.exists(key):
            try:
                return os.path.getmtime(key) + self.__max_age
            except Exception as e:
                raise CacheError(u'{e}: {key}'.format(e=e, key=key))
        else:
            raise CacheError(u'No such file: {key}'.format(key=key))

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
                         encoding=u'UTF-8',
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
                         encoding=u'UTF-8',
                         mode=u'r') as cached_file:
            return self.decode(cached_file.read())

    def delete_by_key(self,
                      key):
        """
        Delete a file from the cache.

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param key: full path and filename
        """
        if os.path.exists(key):
            try:
                return os.path.getmtime(key)
            except Exception as e:
                raise CacheError(u'{e}: {key}'.format(e=e, key=key))
        else:
            raise CacheError(u'No such file: {key}'.format(key=key))

    def delete(self,
               **params):
        """
        Delete a file from the cache.

        NOT INDENTED FOR RE-IMPLEMENTION IN SUBCLASS

        :param params: list of parameters required to
                       fetch the item and create a key
        """
        self.delete_by_key(self.key(**params))
