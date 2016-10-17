# -*- coding: utf-8 -*-
"""
asyncpg
======

Momoko wraps Psycopg2's functionality for use in Tornado.

Copyright 2011-2014, Frank Smit & Zaar Hai.
MIT, see LICENSE for more details.
"""
import logging

import psycopg2

from .connection import Connection, connect
from .exceptions import PoolError, PartiallyConnectedError
from .pool import Pool


try:
    psycopg2.extensions.POLL_OK
except AttributeError:
    import warnings
    warnings.warn(RuntimeWarning(
        'Psycopg2 does not have support for asynchronous connections. '
        'You need at least version 2.2.0 of Psycopg2 to use Momoko.'))

