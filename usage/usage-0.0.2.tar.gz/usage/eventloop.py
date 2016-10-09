#!/usr/bin/env python
# coding: utf8

import time
from xtls.codehelper import singleton


@singleton
class EventLoop(object):

    def __init__(self):
        self._stopping = False

    def stop(self):
        self._stopping = True

    def run(self):
        n = 0
        while not self._stopping:
            print 'hello, world', n
            time.sleep(1)
            n += 1
