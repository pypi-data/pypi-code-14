# -*- coding: utf-8 -*-

'''
QueueIO Queue-like File Buffer Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the QueueIO class

:copyright: (c) 2016 Nick Anderegg
:license: GPLv3, see LICENSE
'''

__title__= 'queueio'
__version__ = '0.1.0'
__author__ = 'Nick Anderegg'
__license__ = 'GPL-3.0'
__copyright__ ='Copyright 2016 Nick Anderegg'

from io import BytesIO
import threading
import hashlib

class QueueIO(BytesIO):
    def __init__(self, max_size=None):

        self.maximum_size   = 1024**3 if max_size is None else max_size

        self.queue_read     = 0
        self.queue_write    = 0

        self.written_bytes  = 0
        self.written_count  = 0
        self.read_bytes     = 0
        self.read_count     = 0

        self.write_hash = hashlib.md5()
        self.read_hash  = hashlib.md5()

        BytesIO.__init__(self)

        self.lock = threading.RLock()

    def __len__(self):
        return self.queue_write - self.queue_read

    def capacity(self):
        return self.maximum_size - len(self)

    def sequential_capacity(self):
        return self.maximum_size - self.queue_write

    def read(self, size=-1):
        size = int(size)
        if self.closed:
            raise ValueError('Attempt to read from closed queue')
        elif size < 0 or size > len(self):
            size = len(self)
        elif size == 0:
            return b''

        with self.lock:
            super().seek(self.queue_read)
            self.queue_read += size

            self.read_bytes += size
            self.read_count += 1

            b = super().read(size)
            self._update_read_hash(b)
            return b

    def write(self, b):
        if len(b) > self.capacity():
            raise ValueError('Attempted to write number of bytes larger than queue capacity')
        elif len(b) > self.sequential_capacity():
            if self._reseat_queue() < len(b):
                return False
        elif self.queue_read > self.sequential_capacity():
            if self._reseat_queue() < len(b):
                return False

        if self.capacity() > self.sequential_capacity() * 1.5:
            self._reseat_queue()

        self._update_write_hash(b)
        with self.lock:
            super().seek(self.queue_write)

            self.queue_write += len(b)

            self.written_bytes += len(b)
            self.written_count += 1

            return super().write(b)

    def _update_read_hash(self, b, thread=False):
        if thread is False:
            threading.Thread(target=self._update_read_hash, args=(b,True)).start()
            return
        else:
            self.read_hash.update(b)
            return

    def _update_write_hash(self, b, thread=False):
        if thread is False:
            threading.Thread(target=self._update_write_hash, args=(b,True)).start()
            return
        else:
            self.write_hash.update(b)
            return

    def _reseat_queue(self):
        with self.lock:
            self.flush()

            queue_size = len(self)

            buff = self.getbuffer()
            buff[0:queue_size] = buff[self.queue_read:self.queue_write]
            del buff

            self.queue_write = queue_size
            self.queue_read = 0

        return self.sequential_capacity()
