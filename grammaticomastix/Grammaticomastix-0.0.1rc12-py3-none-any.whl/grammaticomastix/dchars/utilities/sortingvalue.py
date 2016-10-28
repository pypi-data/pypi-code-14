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
    ❏DChars❏ : dchars/sortingvalue.py
"""

################################################################################
class SortingValue(list):
    """
        class SortingValue

        Class used to compare the "alphabetic" order of two words. A SortingValue
        object contains the "alphabetical" weight of a word as a list of integers.

        [1,2,3] < [99,]
        [1,2] < [1,2,3]
    """

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, aliud):
        """
                SortingValue.__eq__
        """
        return list.__eq__(self, aliud)

    #///////////////////////////////////////////////////////////////////////////
    def __ge__(self, aliud):
        """
                SortingValue.__ge__
        """
        if self == aliud:
            return True

        return SortingValue.__gt__(self, aliud)

    #///////////////////////////////////////////////////////////////////////////
    def __gt__(self, aliud):
        """
                SortingValue.__gt__
        """
        res = None      # =None if equality, False if inferior, True if superior

        for index_element, element in enumerate(self):

            if index_element >= len(aliud):
                res = True
                break

            elif element > aliud[index_element]:
                res = True
                break

            elif element < aliud[index_element]:
                res = False
                break

        if res is None:
            if len(self) > len(aliud):
                res = True
            else:
                res = False

        return res

    #///////////////////////////////////////////////////////////////////////////
    def __le__(self, aliud):
        """
                SortingValue.__le__
        """
        if self == aliud:
            return True

        return SortingValue.__lt__(self, aliud)

    #///////////////////////////////////////////////////////////////////////////
    def __lt__(self, aliud):
        """
                SortingValue.__lt__
        """
        res = None      # =None if equality, False if superior, True if inferior

        for index_element, element in enumerate(self):

            if index_element >= len(aliud):
                res = False
                break

            elif element < aliud[index_element]:
                res = True
                break

            elif element > aliud[index_element]:
                res = False
                break

        if res is None:
            if len(self) < len(aliud):
                res = True
            else:
                res = False

        return res

    #///////////////////////////////////////////////////////////////////////////
    def __ne__(self, aliud):
        """
                SortingValue.__ne__
        """
        return list.__ne__(self, aliud)

