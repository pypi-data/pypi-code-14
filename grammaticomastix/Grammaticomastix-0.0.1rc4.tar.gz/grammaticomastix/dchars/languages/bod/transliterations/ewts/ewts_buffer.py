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
    ❏DChars❏ : dchars/languages/bod/transliterations/ewts/ewts_buffer.py
"""
import os.path

#...............................................................................
# global variables used to buffer the get_intstruct_from_trans_str() function.
#...............................................................................
EWTS_BUFFER_LOADED = False

EWTS_BUFFER__FROM_TRANS_STR = {}          # -> get_intstruct_from_trans_str()
EWTS_BUFFER__FROM_TRANS_STR__FNAME = os.path.join( os.path.abspath( os.path.dirname(__file__)),
                                                   "ewts_buffer_trans_str.data" )


