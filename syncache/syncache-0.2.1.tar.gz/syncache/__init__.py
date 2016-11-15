#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A Python module for basic synchronization between two resources

This module has been conceived for synchronization between
a resource located in a given URI and a temporary folder.
The purpose of this temporary folder is fast loading of
data in grid computing environments, so your scripts can
synchronize the data from a remote machine (or a shared
but slow folder) into a local and faster disk folder.
Once your task finished, it is possible to reverse the
synchronization for any output file produce during the
computation.

Usage Examples

>>> syn = SynCache("/home/user", "/tmp/dest")
>>> syn.sync()
>>> syn.getpath("sample.txt")
'/tmp/dest/sample.txt'
>>> syn.reverse_sync()

>>> syn = SynCache("/home/user", gen_hashed_folder(sys.argv))
>>> syn.getpath("sample.txt")
'/tmp/syncache-6s7fWriA9vSwnMzXsFfSuw=='
"""

__version__ = '0.2.1'

__author__ = 'Francisco Zamora-Martinez'
__copyright__ = 'Copyright 2016, Francisco Zamora-Martinez'
__credits__ = []
__license__ = 'MIT'
__maintainer__ = 'Francisco Zamora-Martinez'
__email__ = 'pakozm@gmail.com'
__status__ = 'Development' # Production when ready for it

import base64
import hashlib
import logging as log
import os
import sys
import tempfile

def _os_system(command):
    log.debug(command)
    result = os.system(command)
    if result != 0:
        raise EnvironmentError("rsync terminated with errors")

def gen_hashed_folder(args=None, prefix=os.path.join(os.sep, "tmp","syncache-")):
    if args is None:
        args = sys.argv
    return prefix + base64.urlsafe_b64encode(hashlib.md5('#'.join(tuple(args))).digest())

class SynCache(object):
    """Simple class for rsync-like folder copy

    This class allows to sync folders from a given URI to a
    temporary folder in the host machine. By calling sync()
    and reverse_sync() it is possible to synchronize both
    resources. By using getpath(filename) it is possible to
    retrieve the desired file path from the temporary folder.
    """

    def __init__(self, source_uri=os.getenv("HOME"),
                 temp_folder=None,
                 verbose=False,
                 temp_prefix='syncache-'):
        """Creates the object for sync. between source_uri and temp_folder

        If not given, temp_folder will be created by means of
        tempfile.mkdtemp(prefix=temp_prefix).
        
        It can be created using function gen_hashed_folder(args_list),
        which returns a 'digested' folder name based on the given
        arguments list.
        
        Raises ValueError in case of failure.
        """
        if temp_folder is None:
            temp_folder = tempfile.mkdtemp(prefix=temp_prefix)
        self._source_uri = source_uri
        self._temp_folder = os.path.abspath(temp_folder)
        flags = ["a"]
        if verbose:
            flags.append("v")
        self._flags = ''.join(flags)

    def sync(self):
        """Executes synchronization into the temporary folder"""
        command = "rsync -%s '%s' '%s'" \
                  % (self._flags, self._source_uri, self._temp_folder)
        _os_system(command)

    def reverse_sync(self):
        """Synchronizes source with temporary folder content"""
        command = "rsync -%s '%s' '%s'" \
                  % (self._flags, self._temp_folder, self._source_uri)
        _os_system(command)

    def getpath(self, source_relative_path):
        """Returns the path of the resource in the temporary folder"""
        temp_dest = os.path.join(self._temp_folder, source_relative_path)
        return temp_dest
