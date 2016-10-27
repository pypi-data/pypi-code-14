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
    ❏DChars❏ : dchars/lstringtools.py

    Utilities for list of strings.
"""

#///////////////////////////////////////////////////////////////////////////////
def no_iterates(seq):
    """
        seq     :       list,tuple

        return <seq> without the duplicates
    """
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

#///////////////////////////////////////////////////////////////////////////////
def sort_a_lstrings_bylen(src):
    """
        src     :       list of strings

        This function sorts <src> first by length and then by contain.

        sort_by_length(("a", "th", "t", "tz", "z", "ze", "aaa", "FH", "F") )
        = ('F', 'a', 't', 'z', 'FH', 'th', 'tz', 'ze', 'aaa')
    """
    string_and_length = [ (len(string), string) for string in src ]
    string_and_length.sort()
    return tuple(zip(*string_and_length))[1]

#///////////////////////////////////////////////////////////////////////////////
def isort_a_lstrings_bylen_nodup(src):
    """
        src     :       list of strings

        This function removes duplicates from src, sorts <src> first by length and
        then by contain and returns the inverse list of sort_a_lstrings_bylen().
    """
    if len(src)==0:
        return src
    return sort_a_lstrings_bylen( no_iterates(src) )[::-1]

#///////////////////////////////////////////////////////////////////////////////
def number_of_occurences( source_string,
                          symbols = None):
    """
        function number_of_occurences()

        Count the number of time the symbol(s) occured in <source_string>.

        source_string   : str
        symbols         : list of strings
    """
    if source_string is None:
        return 0

    nbr = 0

    for char in source_string:
        if char in symbols:
            nbr += 1

    return nbr

#///////////////////////////////////////////////////////////////////////////////
def prepare_list_to_strformat(src):
    """
        function prepare_list_to_strformat()

        src     :       list of strings

        Return <src> prepared to be used with str.format
    """
    res = []
    for string in src:
        res.append(string)
        res[-1] = res[-1].replace( '}', '}}' )
        res[-1] = res[-1].replace( '{', '{{' )
    return res
