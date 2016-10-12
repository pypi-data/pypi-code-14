#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess
from bubble import bcommon

DEFAULT_PORT = 8587
DEFAULT_HOST = 'localhost'
WATCHDOG_STARTSTOP_TIMEOUT = 0
WATCHDOG_CALL_TIMEOUT = 0.3
MULTICOLUMN_NAME = 'allfiles.out'


def get_hg_hash():
    if not get_hg_hash.hash:
        if hasattr(sys, 'frozen') or hasattr(bcommon, 'frozen'):
            # noinspection PyUnresolvedReferences
            from bubble import frozen
            get_hg_hash.hash = frozen.hg_hash
        else:
            try:
                pipe = subprocess.Popen(['hg', 'id', '-i'], stdout=subprocess.PIPE)
                get_hg_hash.hash = pipe.stdout.read().decode()
            except OSError:
                get_hg_hash.hash = 'unknown'
        get_hg_hash.hash = get_hg_hash.hash.strip()
    return get_hg_hash.hash
get_hg_hash.hash = ''
