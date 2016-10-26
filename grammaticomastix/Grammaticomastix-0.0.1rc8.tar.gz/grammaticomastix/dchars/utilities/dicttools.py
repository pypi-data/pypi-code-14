#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
#    DChars Copyright (C) 2012 Suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of DChars.
#    DChars is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DChars is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DChars.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    ❏DChars❏ : dchars/dicttools.py
"""

# problem with Pylint :
# pylint: disable=E0611
# error : like "No name 'errors' in module 'dchars'"
from dchars.errors.errors import DCharsError

#///////////////////////////////////////////////////////////////////////////////
def invertdict(src, accept_duplicated_values = False):
    """
        invertdict() function

        src                             : dict
        accept_duplicated_values        : bool

        Return the inverted dictionary. If accept_duplicated_values is set to False,
        an exception is raised if the lengths of <src> and <res> are different : it
        means that some values were identical and became a unique key.
    """
    res = {v:k for k, v in src.items()}

    if not accept_duplicated_values and len(res) != len(src):
        values = []
        duplicates = []

        for key in src:
            value = src[key]
            if value in values:
                duplicates.append(value)
            else:
                values.append(value)

        dup = []
        for string in duplicates:
            dup.append( str([(string, str([hex(ord(c))])) for c in string ]) )
        dup = "".join(dup)

        raise DCharsError(
                context = 'dicttools.py::invertdict',
                message = "invertdict() : missing values; duplicates="+dup)

    return res
