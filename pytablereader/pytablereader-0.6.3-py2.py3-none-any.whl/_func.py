# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import os.path

from .error import InvalidFilePathError


def get_extension(file_path):
    try:
        return os.path.splitext(file_path)[1].lstrip(".")
    except AttributeError:
        raise InvalidFilePathError("file path is empty")
