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
    ❏DChars❏ : dchars/languages/bod/buffer.py
"""
import os.path

#...............................................................................
# global variables used to buffer the get_intstruct_from_str() function.
#...............................................................................
BUFFER_LOADED = False

# buffer used to build istructs from unicode strings :
BUFFER__FROM_STR = {}                # -> internalstructure.py::get_intstruct_from_str()
# file name :
BUFFER__FROM_STR__FNAME = os.path.join( os.path.abspath( os.path.dirname(__file__)),
                                        "buffer_str.data" )



