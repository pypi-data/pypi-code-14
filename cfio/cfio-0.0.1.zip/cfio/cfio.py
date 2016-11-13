#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import sys

__author__ = 'Marco Bartel'


class File(object):
    python3 = sys.version_info > (3, 0)

    def __init__(self, filePath=None, mode=None, encoding="utf8"):
        self.filePath = filePath
        self.mode = mode
        self.encoding = encoding
        self.fd = None

    def open(self):
        dirPath = os.path.dirname(self.filePath)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        if self.python3:
            self.fd = open(self.filePath, self.mode, encoding=self.encoding)
        else:
            self.fd = open(self.filePath, self.mode)

    def write(self, data):
        if not self.python3:
            data = data.encode(self.encoding)
        self.fd.write(data)

    def read(self):
        data = self.fd.read()
        if not self.python3:
            data = data.decode(self.encoding)
        return data

    def readlines(self):
        return self.read().splitlines()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()
        return False