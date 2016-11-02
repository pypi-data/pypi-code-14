#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import zlib
import base64
import binascii
import numpy as np


class CompressError(Exception):
    pass


def compress(s):
    return base64.b64encode(zlib.compress(s.encode(), 9))


def compressFile(f):
    try:
        return compress(open(f).read())
    except IOError:
        return ''


def decompress(b64str):
    try:
        return zlib.decompress(base64.b64decode(b64str))
    except (binascii.Error, zlib.error):
        raise CompressError('The string does not seem to be compressed')


def compressNumpyArray(array):
    buf = io.BytesIO()
    # noinspection PyTypeChecker
    np.savez_compressed(buf, array)
    return base64.b64encode(buf.getvalue())


def decompressNumpyArray(array):
    try:
        return np.load(io.BytesIO(base64.b64decode(array)))['arr_0']
    except (TypeError, OSError, binascii.Error):
        return None
