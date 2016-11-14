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

Usage Example

>>> syn = SynCache("/home/user", "/tmp/dest")
>>> syn.sync()
>>> syn.getfilename("sample.txt")
/tmp/dest/sample.txt
>>> syn.reverse_sync()
"""

__version__ = '0.1.0'

__author__ = 'Francisco Zamora-Martinez'
__copyright__ = 'Copyright 2016, Francisco Zamora-Martinez'
__credits__ = []
__license__ = 'MIT'
__maintainer__ = 'Francisco Zamora-Martinez'
__email__ = 'pakozm@gmail.com'
__status__ = 'Development' # Production when ready for it

import logging as log
import os
import tempfile

def _os_system(command):
    log.debug(command)
    result = os.system(command)
    if result != 0:
        raise EnvironmentError("rsync terminated with errors")

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
                 verbose=False):
        """Creates the object for sync. between source_uri and temp_folder

        If not given, temp_folder will be created by means of
        tempfile.mkdtemp(prefix='diskcache')
        
        Raises ValueError in case of failure.
        """
        if temp_folder is None:
            temp_folder = tempfile.mkdtemp(prefix='diskcache')
        self._source_uri = source_uri
        self._temp_folder = os.path.abspath(temp_folder)
        flags = ["a"]
        if verbose:
            flags.append("v")
        self._flags = ''.join(flags)
        if not os.path.isdir(self._temp_folder):
            raise ValueError("temp_folder %s should be a directory"
                             % self._temp_folder)

    def sync(self):
        """Executes synchronization into the temporary folder"""
        command = "rsync -%s '%s' '%s'" \
                  % (flags, self._source_uri, self._temp_folder)
        _os_system(command)

    def reverse_sync(self):
        """Synchronizes source with temporary folder content"""
        command = "rsync -%s '%s' '%s'" \
                  % (flags, self._temp_folder, self._source_uri)
        _os_system(command)

    def getpath(self, source_relative_path):
        """Returns the path of the resource in the temporary folder"""
        temp_dest = os.path.join(self._temp_folder, source_relative_path)
        return temp_dest
