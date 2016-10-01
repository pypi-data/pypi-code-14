#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict, MutableSet, Sequence


class OrderedSet(MutableSet):
    def __init__(*args):
        self, *args = args
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))

        self._dict = OrderedDict(((key, None) for key in args[0]) if args else {})

    def __iter__(self):
        return (k for k in self._dict)

    def __reversed__(self):
        return (k for k in reversed(self._dict))

    def first(self):
        if not self:
            raise KeyError('ordered set is empty')

        return next(iter(self))

    def last(self):
        if not self:
            raise KeyError('ordered set is empty')

        return next(reversed(self))

    def __contains__(self, x):
        return self._dict.__contains__(x)

    def __len__(self):
        return self._dict.__len__()

    def add(self, value):
        self._dict[value] = None

    def discard(self, value):
        del self._dict[value]

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return self._dict == other._dict

        if isinstance(other, Sequence):
            if len(other) != len(self):
                return False

            it = iter(self)
            for other_v in other:
                v = next(it)
                if v != other_v:
                    return False

            return True

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, [v for v in self._dict])


oset = OrderedSet
odict = OrderedDict


def inherit_doc(cls):
    if isinstance(cls, type):
        if not cls.__doc__:
            for mro_type in cls.__mro__:
                if mro_type.__doc__ and mro_type not in (cls, object):
                    cls.__doc__ = mro_type.__doc__
                    break

        for name, member in cls.__dict__.items():
            if member and (not member.__doc__ or isinstance(member, (classmethod, staticmethod))):
                for mro_type in cls.__mro__:
                    if mro_type not in (cls, object):
                        mro_member = mro_type.__dict__.get(name)
                        if mro_member and mro_member.__doc__:
                            if isinstance(member, (classmethod, staticmethod)):
                                member = member.__func__
                            if isinstance(mro_member, (classmethod, staticmethod)):
                                mro_member = mro_member.__func__

                            member.__doc__ = mro_member.__doc__
                            break
        return cls
    else:
        raise RuntimeError("only full class documentation inheritance is supported")
