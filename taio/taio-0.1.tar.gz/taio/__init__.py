# -*- coding: utf-8 -*-
"""Twisted AIO module.
"""
from .core import taioError, taioContext
from twisted.internet.abstract import FileDescriptor
from twisted.internet.interfaces import IReadDescriptor
from twisted.internet import reactor
from zope.interface import implements
import os
from twisted.python import log


class AIOScheduler(FileDescriptor):
    """This is layer responsible for scheduling aio requests
    to kernel.
    """
    implements(IReadDescriptor)

    def __init__(self, maxRequests=128, _reactor=None):
        """This is layer responsible for scheduling aio requests
        to kernel.
        Args:
            maxRequests: max nr of AIO requests.
            _reactor: if Nonestandard twisted reactor is used.
        """
        self._fd = None
        if _reactor is None:
            _reactor = reactor
        self.clock = _reactor
        FileDescriptor.__init__(self, _reactor)
        self.ctx = taioContext(maxRequests)
        self.stringEncoder = 'utf-8'

    def startReading(self):
        ''' do not use this directly '''
        raise NotImplementedError("Should never be called")

    def fileno(self):
        ''' returns eventfd fileno '''
        return self.ctx.fileno()

    def doRead(self):
        '''complete AIO events
         do not use this directly '''
        try:
            self.ctx.event()
        except RuntimeError as err:
            log.err("failed with error %s" % err)
            raise err

    def doWrite(self):
        raise NotImplementedError("Should never be called")

    def connectionLost(self, reason):
        FileDescriptor.connectionLost(self, reason)

    def logPrefix(self):
        return "%s " % (self.__class__.__name__)

    def start(self):
        ''' start scheduler '''
        self.clock.addReader(self)

    def stop(self):
        '''stop scheduler '''
        self.clock.removeReader(self)
        self.ctx.stop()

    def setEncode(self, encode):
        ''' set encode coversion for unicode string  default utf-8'''
        self.stringEncoder = encode

    def open(self, path, mode):
        ''' open new AIO file object '''
        if isinstance(path, unicode):
            path = path.encode(self.stringEncoder)
        return  self.ctx.open(path, mode)
