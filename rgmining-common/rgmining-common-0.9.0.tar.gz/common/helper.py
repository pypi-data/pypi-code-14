#
# helper.py
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
"""Mixins for algebraic classes.
"""
import copy
import json


class ImmutableAdditiveGroup(object):

    # Needs, __add__, __neg__, __eq__,

    def __add__(self, _):
        raise NotImplementedError("Subclasses must implement __add__.")

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        raise NotImplementedError("Subclasses must implement __neg__.")

    def __eq__(self, _):
        raise NotImplementedError("Subclasses must implement __eq__.")

    def __ne__(self, other):
        return not self == other


class MultipliableImmutableAdditiveGroup(ImmutableAdditiveGroup):

    # Needs, __add__, __rmul__, __eq__,

    def __rmul__(self, _):
        # value must be a number.
        raise NotImplementedError("Subclasses must implement __rmul__")

    def __div__(self, value):
        # value must be a number.
        return (1./value) * self

    def __neg__(self):
        return -1 * self


class JSONable(object):

    def __json__(self):
        raise NotImplementedError("Subclasses must implement __json__")

    def __str__(self):
        return json.dumps(self.__json__())


class ImmutableMathHelper(object):

    # add, mul, div, eq
    def __add__(self, _):
        raise NotImplementedError("Subclasses must implement __add__.")

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return -1 * self

    def __eq__(self, _):
        raise NotImplementedError("Subclasses must implement __eq__.")

    def __ne__(self, other):
        return not self.__eq__(other)


class MathHelper(ImmutableMathHelper):

    # iadd, imul, idiv, neg, eq, __deepcopy__
    def __iadd__(self, _):
        raise NotImplementedError("Subclasses must implement __iadd__.")

    def __add__(self, other):
        res = copy.deepcopy(self)
        res += other
        return res

    def __isub__(self, other):
        self.__iadd__(-other)
        return self

    def __mul__(self, other):
        res = copy.deepcopy(self)
        res *= other
        return res

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        res = copy.deepcopy(self)
        res /= other
        return res
