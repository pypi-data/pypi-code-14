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
    ❏DChars❏ : dchars/orderedset.py

    code from http://code.activestate.com/recipes/576694/
"""

# problem with Pylint :
# pylint: disable=E0611
# "No name 'errors' in module 'dchars.errors'"
from dchars.errors.errors import DCharsError
import collections

################################################################################
class OrderedSet(collections.MutableSet):
    """
        class OrderedSet

        originally from http://code.activestate.com/recipes/576694/
    """

    #///////////////////////////////////////////////////////////////////////////
    def __contains__(self, key):
        """
                OrderedSet.__contains__
        """
        return key in self.map

    # #///////////////////////////////////////////////////////////////////////////
    # def __deepcopy__(self, memo):
    #     """
    #             OrderedSet.__deepcopy__
    #
    #             This is NOT a correct implementation of a __deepcopy__ method
    #             since this function doesn't take <memo> in account.
    #     """
    #     newone = type(self)( list(self.map) )
    #     return newone

    #///////////////////////////////////////////////////////////////////////////
    def __init__(self, iterable=None):
        """
                OrderedSet.__init__
        """
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, _prev, _next]
        if iterable is not None:
            self |= iterable

    #///////////////////////////////////////////////////////////////////////////
    def __iter__(self):
        """
                OrderedSet.__iter__
        """
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    #///////////////////////////////////////////////////////////////////////////
    def __len__(self):
        """
                OrderedSet.__len__
        """
        return len(self.map)

    #///////////////////////////////////////////////////////////////////////////
    def __eq__(self, other):
        """
                OrderedSet.__eq__
        """
        if other is None:
            return False
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    #///////////////////////////////////////////////////////////////////////////
    def __repr__(self):
        """
                OrderedSet.__repr__
        """
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    #///////////////////////////////////////////////////////////////////////////
    def __reversed__(self):
        """
                OrderedSet.__reversed__
        """
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    #///////////////////////////////////////////////////////////////////////////
    def add(self, key):
        """
                OrderedSet.add
        """
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    #///////////////////////////////////////////////////////////////////////////
    def discard(self, key):
        """
                OrderedSet.discard
        """
        if key in self.map:
            key, _prev, _next = self.map.pop(key)
            _prev[2] = _next
            _next[1] = _prev

    # problem with Pylint : list.pop() DO have one argument
    # pylint: disable=W0221
    # Arguments number differs from overriden method
    #///////////////////////////////////////////////////////////////////////////
    def pop(self, last=True):
        """
                OrderedSet.pop
        """
        if not self:
            raise DCharsError( context = "OrderedSet.pop",
                               message = "<self> is an empty set. self="+str(self) )

        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    #///////////////////////////////////////////////////////////////////////////
    def update(self, keys):
        """
                OrderedSet.update
        """
        for key in keys:
            self.add(key)



