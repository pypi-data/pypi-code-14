#
# __init__.py
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
"""Provide common classes and functions.

The common module and its submodules probides varies functions ans classes
which can be used in any context.

Functions
------------
This module provides the following functions which are alias of ones in
sub-modules.

:func:`print_args <common.decorator.print_args>`
    Decorate a function so that print arguments before calling it.
:func:`print_return <common.decorator.print_return>`
    Decorate a function so that print result after calling it.
:func:`constant <common.decorator.constant>`
    Decorate a function so that the result is a constant value.
:func:`memoized <common.decorator.memoized>`
    Decorate a function to memoize results.
"""
from __future__ import absolute_import
from common.decorator import print_args
from common.decorator import print_return
from common.decorator import constant
from common.decorator import memoized
