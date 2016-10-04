#
# decorator.py
#
# Copyright (c) 2016 Junpei Kawamoto
#
# This file is part of rgmining-common.
#
# rgmining-common is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-common is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#
"""Defines common decorators.

This module provides useful decorators.
"""
import gc
from functools import wraps
import sys


def print_args(output=sys.stdout):
    """Decorate a function so that print arguments before calling it.

    Args:
      output: writable to print args. (Default: sys.stdout)
    """
    def decorator(func):
        """The decorator function.
        """
        @wraps(func)
        def _(*args, **kwargs):
            """The decorated function.
            """
            output.write(
                "Args: {0}, KwArgs: {1}\n".format(str(args), str(kwargs)))
            return func(*args, **kwargs)
        return _
    return decorator


def print_return(output=sys.stdout):
    """Decorate a function so that print result after calling it.

    Args:
      output: writable to print return values. (Default: sys.stdout)
    """
    def decorator(func):
        """The decorator.
        """
        @wraps(func)
        def _(*args, **kwargs):
            """The decorated function.
            """
            res = func(*args, **kwargs)
            output.write("Return: {0}\n".format(str(res)))
            return res
        return _
    return decorator


def constant(func):
    """Decorate a function so that the result is a constant value.

    Functions wraped by this decorator will be run just one time.
    The computational result will be stored and reused for any other input.

    To store each result for each input, use :func:`memoized` instead.
    """
    @wraps(func)
    def _(*args, **kwargs):
        """The decorated function.
        """
        if not _.res:
            _.res = func(*args, **kwargs)
        return _.res
    _.res = None
    return _


def memoized(func):
    """Decorate a function to memoize results.

    Functions wraped by this decorator won't compute twice for each input.
    Any results will be stored. This decorator might increase used memory
    in order to shorten computational time.
    """
    cache = {}
    @wraps(func)
    def memoized_function(*args):
        """The decorated function.
        """
        try:
            return cache[args]
        except KeyError:
            value = func(*args)
            try:
                cache[args] = value
            except MemoryError:
                cache.clear()
                gc.collect()
            return value
    return memoized_function
