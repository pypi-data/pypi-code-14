# -*- coding: utf-8 -*-

'''
DownloadBuffer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements the DownloadBuffer class

:copyright: (c) 2016 Nick Anderegg
:license: GPLv3, see LICENSE
'''

__title__= 'downloadbuffer'
__version__ = '0.1.4'
__author__ = 'Nick Anderegg'
__license__ = 'GPL-3.0'
__copyright__ ='Copyright 2016 Nick Anderegg'

import requests
from requests.packages.urllib3.exceptions import *
from requests.exceptions import *

import threading
import time

from base64 import b64decode
from hashlib import md5

from queueio import QueueIO

class DownloadBuffer(QueueIO):
    def __init__(self, url, max_size=None):
        QueueIO.__init__(self, max_size)

        self.url = url
        self.request = requests.Request('GET', url=self.url).prepare()

        self.session = requests.Session()
        self.session.stream = True

        self.download_bytes = 0
        self.download_duration = 0
        self.download_start_time = 0
        self.download_end_time = False
        self.download_hash = md5()

        self.live = threading.Event()
        self.live.set()

        self.initialized = False

    def initialize(self):
        self.get_headers()
        self.get_raw()
        self.initialized = True

    def start(self, chunk_size=1024**2):
        if not self.initialized:
            self.initialize()

        if self.initialized:
            self._start_downloading(chunk_size=chunk_size)

    def get_headers(self):
        request = self.request.copy()
        request.method = 'HEAD'

        response = self.session.send(request)
        if response.status_code != requests.codes.ok:
            raise ConnectionError()

        headers = response.headers

        if 'x-goog-hash' in headers:
            md5hash = headers['x-goog-hash'].find('md5=') + 4
            md5hash = headers['x-goog-hash'][md5hash:md5hash+24]
            self.md5hash = b64decode(md5hash).hex()


        self.content_length = int(headers['Content-Length'])
        # print(self.unitizer(self.content_length, 'B', True))

    def get_raw(self, first_byte=None):
        request = self.request.copy()

        if first_byte is not None:
            if first_byte == self.content_length:
                return True
            request.headers['Range'] = 'bytes={}-{}'.format(first_byte, self.content_length)

        start_time = time.perf_counter()
        try:
            response = self.session.send(request, timeout=(9.10, 27))
        except ConnectionError:
            if first_byte is not None:
                return False
            else:
                raise

        if first_byte is None and response.status_code != requests.codes.ok:
            raise ConnectionError()
        elif first_byte is not None and response.status_code != requests.codes.partial:
            if (response.status_code == 416 and
                self.download_bytes == self.content_length and
                self.md5hash == self.download_hash.hexdigest()):
                return True
            raise ConnectionError()
        self.download_duration += (time.perf_counter() - start_time)

        self.raw_stream = response.raw
        return True

    def write(self, b):
        write_start = time.perf_counter()
        super().write(b)
        self.write_duration += (time.perf_counter() - write_start)

    def write_speed(self):
        return self.written_bytes / self.write_duration

    def read(self, size=-1, timeout=None):
        size = int(size)
        if size > self.maximum_size:
            raise ValueError('Read size cannot be larger than buffer')
        elif size < 0:
            if self.written_bytes == self.content_length:
                size = len(self)
            elif (self.content_length - self.read_bytes) < self.maximum_size:
                size = self.content_length - self.read_bytes
            else:
                raise ValueError('Read length cannot be undefined when pending download is larger than buffer')
        elif size > self.content_length - self.read_bytes:
            size = self.content_length - self.read_bytes

        wait_count = 0
        wait_duration = float(0)
        while size > len(self):
            if timeout is not None and wait_duration > timeout:
                raise TimeoutError('Read took longer than timeout')
            time.sleep((1.2**wait_count)*.00001)
            wait_duration += (1.2**wait_count)*.00001
            wait_count += 1

        read_start = time.perf_counter()
        if self.read_bytes == self.content_length:
            print('Read bytes are content length')
            self.close()
        return super().read(size)


    def _start_downloading(self, chunk_size=1024**2):
        self.download_start_time = time.perf_counter()
        self.download_thread = threading.Thread(target=self._download_thread, args=(chunk_size,))
        self.download_thread.start()
        return

    def reestablish_connection(self, max_retries=9):
        first_byte = self.written_bytes
        for i in range(max_retries):
            print('Attempting to reconnect...')
            raw = self.get_raw(first_byte)
            if raw is False:
                print('Attempt to reconnect failed, retrying in {:.3f}s'.format(2**(i+1)))
                time.sleep(2**(i+1))
            else:
                print('Connection re-established.')
                return True

        return False


    def _download_thread(self, chunk_size=1024**2):
        wait_count = 0
        while self.live.is_set():
            while self.capacity() > 0 and self.capacity() < chunk_size:
                chunk_size = round(chunk_size/2)
                if chunk_size < 1:
                    chunk_size = 1

            if self.capacity() > 0:
                wait_count = 0
                if self._download_chunk(chunk_size):
                    continue
                elif (
                        self.download_bytes == self.content_length and
                        self.md5hash == self.download_hash.hexdigest()
                ):
                    self.download_end_time = time.perf_counter()
                    self.live.clear()
                    return
                else:
                    print('Connection to server lost')
                    self.reestablish_connection()
            else:
                time.sleep((1.1**wait_count)*.00001)
                wait_count += 1


    def _download_chunk(self, chunk_size=1024**2):
        if not self.raw_stream.closed:
            try:
                start_time = time.perf_counter()
                chunk = self.raw_stream.read(chunk_size)
                self.download_duration += (time.perf_counter() - start_time)

                self.write(chunk)
                self.download_bytes += len(chunk)
                self._update_download_hash(chunk)

                return True
            except:
                return False
        else:
            print('Raw is closed. File size:', self.unitizer(self.content_length, 'B', True), 'Read:', self.unitizer(self.written_bytes, 'B', True))
            return False

    def _update_download_hash(self, b, thread=False):
        if thread is False:
            threading.Thread(target=self._update_download_hash, args=(b,True)).start()
            return
        else:
            self.download_hash.update(b)
            return

    def download_speed(self):
        return self.download_bytes/self.download_duration

    def overall_speed(self):
        if not self.download_end_time:
            return self.download_bytes/(time.perf_counter()-self.download_start_time)
        else:
            return self.download_bytes/(self.download_end_time-self.download_start_time)

    # Debug tools
    def print_download_statistics(self):
        download_speed = self.download_speed()
        print('----------')
        print('File size: {}\tProgress:{:.2f}%\tEst: {:0>2d}h{:0>2d}m{:0>2d}s remaining'.format(
            self.unitizer(self.content_length, 'B', True),
            self.download_bytes/self.content_length*100,
            int((self.content_length-self.download_bytes) / download_speed / 3600) if download_speed > 0 else 0,
            int((self.content_length-self.download_bytes) / download_speed % 3600 / 60) if download_speed > 0 else 0,
            int((self.content_length-self.download_bytes) / download_speed % 60) if download_speed > 0 else 0
        ))
        print('Final file hash:\t\t\t{}'.format(self.md5hash))
        print('Written bytes:\t  {:>9}\tDigest: {}'.format(self.unitizer(self.written_bytes, 'B', True), self.write_hash.hexdigest()))
        print('Read bytes:\t  {:>9}\tDigest: {}'.format(self.unitizer(self.read_bytes, 'B', True), self.read_hash.hexdigest()))
        print('Downloaded:\t  {:>9}\tDigest: {}'.format(self.unitizer(self.download_bytes, 'B', True), self.download_hash.hexdigest()))#self.download_bytes/1000**2))
        print('Download only:\t{:>11}/s'.format(self.unitizer(download_speed, 'b', True)))
        print('Total duration:\t{:>11}/s'.format(self.unitizer(self.overall_speed(), 'b', True)))
        print()

    def test_flow(self):
        self.initialize()
        # try:
        self.test_thread = threading.Thread(target=self._test_flow)
        print('Starting test flow...')
        self.test_thread.start()
        print('Test flow started...')
        return
        # except KeyboardInterrupt:
        #     self.live.clear()
        #     raise
        #     return

    def _test_flow(self):
        print('Entering test flow thread')
        self.print_download_statistics()
        self.start()
        last_print = -1
        iter_count = 0
        while True:
            iter_count += 1
            time.sleep(1)
            # if len(self) > 0:
                # self.read(1024**2)
                # if self.written_bytes != last_print:
                # if self.written_bytes % 536870912 == 0: #16777216
            if iter_count % 15 == 0:
                print()
                self.print_download_statistics()
                # elif self.written_bytes % 67108864 == 0:
            elif iter_count % 15 == 0:
                download_speed = self.download_speed()
                print('Progress: {:>5.2f}%\tEst: {:0>2d}h{:0>2d}m{:0>2d}s remaining'.format(
                    self.download_bytes/self.content_length*100,
                    int((self.content_length-self.download_bytes) / download_speed / 3600) if download_speed > 0 else 0,
                    int((self.content_length-self.download_bytes) / download_speed % 3600 / 60) if download_speed > 0 else 0,
                    int((self.content_length-self.download_bytes) / download_speed % 60) if download_speed > 0 else 0
                ))
                    # last_print = self.written_bytes

        self.print_download_statistics()

        self.live.clear()

    def unitizer(self, b, unit='b', metric=False, time=None):
        if metric:
            kilo = 1000
            prefix_i = ''
        else:
            kilo = 1024
            prefix_i = 'i'

        if unit == 'b':
            multiplier = 8
        else:
            multiplier = 1

        if time is not None:
            b = b / time
            time_suffix = '/s'
        else:
            time_suffix = ''

        if b >= kilo**5:
            return '{:.2f} P{}{}{}'.format(((b/kilo**5)*multiplier), prefix_i, unit, time_suffix)
        elif b >= kilo**4:
            return '{:.2f} T{}{}{}'.format(((b/kilo**4)*multiplier), prefix_i, unit, time_suffix)
        elif b >= kilo**3:
            return '{:.2f} G{}{}{}'.format(((b/kilo**3)*multiplier), prefix_i, unit, time_suffix)
        elif b >= kilo**2:
            return '{:.2f} M{}{}{}'.format(((b/kilo**2)*multiplier), prefix_i, unit, time_suffix)
        elif b >= kilo:
            return '{:.2f} K{}{}{}'.format(((b/kilo**2)*multiplier), prefix_i, unit, time_suffix)
        else:
            return '{:.2f}  {}{}{}'.format((b*multiplier), prefix_i, unit, time_suffix)
