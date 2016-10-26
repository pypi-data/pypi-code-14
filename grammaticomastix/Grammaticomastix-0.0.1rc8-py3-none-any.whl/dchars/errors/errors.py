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
    ❏DChars❏ : dchars/errors/errors.py
"""

#///////////////////////////////////////////////////////////////////////////////
def display_error( context, message ):
    """
        function display_error
    """

    print("="*80)
    print( "({0}) {1}".format(context, message))
    print("="*80)

################################################################################
class DCharsError(BaseException):
    """
        class DCharsError

        All purpose class.
    """

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, context, message):
        """
                DCharsError.__init__
        """
        BaseException.__init__(self, message)

        display_error("[DCharsError] "+context,
                      message)

