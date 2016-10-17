# -*- coding: utf-8 -*-
"""
asyncpg.exceptions
=================

Exceptions.

Copyright 2011-2014, Frank Smit & Zaar Hai.
MIT, see LICENSE for more details.
"""


class PoolError(Exception):
    """
    Raised when something goes wrong in the connection pool.
    """
    pass


class PartiallyConnectedError(PoolError):
    """
    Raised  when :py:meth:`asyncpg.Pool` can not initialize all of the requested connections.
    """