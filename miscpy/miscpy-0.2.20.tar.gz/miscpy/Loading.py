#!/usr/bin/python
# -*- coding: utf8 -*-

"""
Functions and classes for easier file handling during loading.
:author: Manuel Tuschen
:license: FreeBSD

License
----------
Copyright (c) 2016, Manuel Tuschen
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


from __future__ import division, absolute_import, unicode_literals, print_function
import os
import glob

from .Saving import extractFromFilename


__all__ = ["prepareLoading", "multiLoading"]


def prepareLoading(filename, path="", extension=""):
    """
    Prepare for loading a file.
    The filename may already include the path. If "path" is given, the filename
    must be relative to "path". If no absolute path is set either in the
    filename with "path", the current working directory is used.
    The filename may also contain an extension separated by a '.'. If
    "extension" is given, this will replace any extension in the filename by
     searching for the last '.' and replacing the exceeding string.
    If the file to load does not exists, an IOError is thrown.

    Parameters
    ----------
    filename : string
        The name of the file to load
    path : string, optional
        The path where the file is located. If none is given, the current
        working directory is assumed.
    extension : string, optional
        File extension to append at the filename e.g ".png".

    Returns
    --------
    filename : string
        The full filename including the path and extension.

    Raises
    ------
    IOError :
        If file to load does not exists.
    """

    fname, tmp_path, tmp_ext = extractFromFilename(filename)

    # prepare path
    path = os.path.join(path, tmp_path)
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.exists(path):
        os.makedirs(path)
    # prepare extension
    if len(fname) == 0:
        extension = ""
    elif len(extension) > 0:
        extension = extension.lstrip('.')
        extension = '.' + extension
    elif len(tmp_ext) > 0:
        extension = tmp_ext.lstrip('.')
        extension = '.' + extension
    else:
        extension = ""

    filename = os.path.join(path, fname + extension)
    # check if file exists
    if not os.path.isfile(filename):
        raise IOError('File {f} does not exist'.format(f=filename))

    return filename


def multiLoading(identifier='*', path="", SUBPATH=False):
    """
    Find directories of multiple files.

    Parameters
    ----------
    identifier : string
        String which might contain shell like wildcars to identify the files to
        load.
    path : string, optional
        The path where the file is located. If none is given, the current
        working directory is assumed.
    SUBPATH : bool
        Search also subdirectories.

    Returns
    --------
    filenames : list
        A list with all filenames including the path.
    """

    # prepare path
    if len(path) == 0:
        path = os.getcwd()
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    path = os.path.abspath(os.path.expanduser(path))

    # eventually including subdirectories
    if SUBPATH:
        filenames = []
        for root, dirs, files in os.walk(path, topdown=False):
            new_files = (glob.glob(os.path.join(root, identifier)))
            for file in new_files:
                filenames.append(file)
    else:
        filenames = glob.glob(os.path.join(path, identifier))

    return sorted(filenames)

