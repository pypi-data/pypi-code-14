#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import time
import asyncio
import threading
import traceback
from concurrent import futures
import numpy as np
import cryio
from ..bcommon import compressor, default
from .integrator import Integrator


ATTEMPTS_TO_OPEN = 10


class _ThreadLocal(threading.local):
    integrator = None

    def __init__(self):
        if self.integrator is None:
            self.integrator = Integrator()


class _PeriodicTask:
    def __init__(self, func):
        self.func = func
        self.stop()

    def start(self, interval):
        self.interval = interval
        self.running = True
        asyncio.ensure_future(self._run())

    async def _run(self):
        while self.running:
            await self.func()
            await asyncio.sleep(self.interval)

    def stop(self):
        self.running = False


class Watcher:
    def __init__(self, integrator_interface):
        self.interface = integrator_interface
        self._path = ''
        self.runLocally = False
        self._multicolumnName = ''
        self.all = 0
        self.watchdog = _PeriodicTask(self.checkFiles)
        self._loop = asyncio.get_event_loop()
        self._pool = futures.ThreadPoolExecutor(os.cpu_count() + 1)
        self.__local = None
        self.clearState()

    def clearState(self):
        self.results = {
            'imageFile': '',
            'chiFile': '',
            'transmission': 0,
            'data1d': None,
            'image': None,
            'timestamp': time.time(),
            'sent': True,
        }
        self.errors = []
        self.warnings = []
        self.taken = set()
        self.processed = set()
        self.multicolumn = []
        self.qvalues = None
        self.all = 0
        self.interface.clearState()
        self.generate_response()

    @property
    def path(self):
        return self._path if self._path else 'unknown'

    @path.setter
    def path(self, path):
        if self._path == path:
            return
        elif not os.path.exists(path):
            self.errors.append('The {} path "{}" does not exist'.format(self.interface.type, path))
        elif not os.path.isdir(path):
            self.errors.append('The {} path "{}" is not a folder'.format(self.interface.type, path))
        else:
            self._changePath(path)

    def _changePath(self, path):
        run = self.watchdog.running
        if run:
            self.stopWatching()
        self._path = path
        if run:
            self.runWatching()

    def runWatching(self):
        if not self.watchdog.running:
            self.clearState()
            self.watchdog.start(default.WATCHDOG_CALL_TIMEOUT)

    async def checkFiles(self):
        edfs = glob.glob(os.path.join(self._path, '*.edf'))
        cbfs = glob.glob(os.path.join(self._path, '*.cbf'))
        images = set(edfs + cbfs)
        self.all = len(images)
        images -= self.taken
        if self.interface.speed and self.interface.sspeed:
            self.taken |= images
            for image in images:
                self._loop.run_in_executor(self._pool, self.__thread_wrapper, image)
        else:
            for image in images:
                if not self.watchdog.running:
                    return
                self.taken.add(image)
                await self.integrate(image)

    def __open_image(self, filename):
        i = 0
        while True:
            i += 1
            # noinspection PyBroadException
            try:
                image = cryio.openImage(filename)
                if isinstance(image, cryio.cbfimage.CbfImage) and 'Flux' not in image.header:
                    raise ValueError
            except:
                if i < ATTEMPTS_TO_OPEN:
                    print('File {} could not be read {:d} times, another attempt...'.format(filename, i))
                    time.sleep(1)
                else:
                    traceback.print_exc(file=sys.stdout)
                    print('Frame {} could not be read, see exception above :('.format(filename))
                    return None
            else:
                return image

    def __thread_wrapper(self, filename):
        self.__local = self.__local or _ThreadLocal()
        image = self.__open_image(filename)
        if image:
            return self.__local.integrator(filename, image, self.interface)

    async def integrate(self, image):
        results = await self._loop.run_in_executor(self._pool, self.__thread_wrapper, image)
        if results:
            self.processed.add(image)
            self.results = results
            self.resetSent()
            if self.multicolumnName:
                self.multicolumn.append((results['chiFile'], results['data1d'][1]))
                if self.qvalues is None:
                    self.qvalues = results['data1d'][0]

    def stopWatching(self):
        if self.watchdog.running:
            self.watchdog.stop()
            if self.multicolumn:
                asyncio.ensure_future(self._loop.run_in_executor(self._pool, self.save_multicolumn))

    def save_multicolumn(self):
        arrays, header = [compressor.decompressNumpyArray(self.qvalues)], 'q '
        for fn, ar in sorted(self.multicolumn):
            arrays.append(compressor.decompressNumpyArray(ar))
            header += '{} '.format(os.path.basename(fn))
        subdir = os.path.dirname(self.multicolumn[0][0])
        outf = os.path.join(self._path, subdir, default.MULTICOLUMN_NAME)
        np.savetxt(outf, np.array(arrays).transpose(), header=header, comments='#')

    @property
    def multicolumnName(self):
        return self._multicolumnName

    @multicolumnName.setter
    def multicolumnName(self, name):
        self._multicolumnName = name or ''

    def setParameters(self, params):
        self.interface.errors = self.errors = []
        self.interface.warnings = self.warnings = []
        for param in params:
            setattr(self, param, params[param])
            setattr(self.interface, param, params[param])
        if 'stop' in params:
            self.stopWatching()
        if not self.errors and 'run' in params and params['run'] == 1:
            self.runWatching()

    def state(self):
        return self.generate_response()

    def generate_response(self):
        self.response = {
            'running': self.watchdog.running,
            'chiFile': self.results['chiFile'],
            'path': self.path,
            'total': self.total(),
            'imageFile': self.results['imageFile'],
            'transmission': self.results['transmission'],
            'data1d': None,
            'image': None,
            'timestamp': self.results['timestamp'],
            'all': self.all,
        }
        if not self.results['sent'] and self.results['image'] is not None and self.results['data1d'] is not None:
            self.response['data1d'] = self.results['data1d']
            self.response['image'] = self.results['image']
        return self.response

    def resetSent(self):
        self.results['sent'] = False

    def total(self):
        if self.interface.sspeed:
            return self.interface.speedcounter
        else:
            return len(self.processed)
