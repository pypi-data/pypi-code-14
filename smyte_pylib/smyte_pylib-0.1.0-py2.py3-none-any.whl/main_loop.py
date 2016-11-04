from __future__ import absolute_import

import ctypes
import logging
import signal
import time
from docopt import docopt
from multiprocessing import Value
from pysigset import suspended_signals

logger = logging.getLogger('pylib:service')

class ExitLoop(Exception):
    pass

def main_loop(fn, period=None):
    exit = Value(ctypes.c_bool)

    def sigint_handler(signal, frame):
        print('Picked up interrupt, pausing at next break point')
        exit.value = True
    signal.signal(signal.SIGINT, sigint_handler)

    def sigterm_handler(signal, frame):
        print('Picked up sigterm, pausing at next break point')
        exit.value = True
    signal.signal(signal.SIGTERM, sigterm_handler)

    sleep_until = 0
    while not exit.value:
        if period is not None:
            if time.time() < sleep_until:
                time.sleep(min(1, sleep_until - time.time()))
                continue
            sleep_until = time.time() + period

        with suspended_signals(signal.SIGINT, signal.SIGTERM):
            try:
                fn()
            except ExitLoop:
                break

        if period is not None:
            total_sleep = sleep_until - time.time()
            if total_sleep > 1:
                logger.info('Waiting %.1f until loop period' % total_sleep)
