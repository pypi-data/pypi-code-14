# Copyright 2016 Allen Li
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

import abc


class Monad(abc.ABC):

    @abc.abstractmethod
    def bind(self, f):
        """Haskell: >>="""
        raise NotImplementedError

    def then(self, k):
        """Haskell: >>"""
        return self.bind(lambda _: k)


class MonadicMonad(Monad):

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return '{}({!r})'.format(type(self).__qualname__, self._value)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._value == other._value
        else:
            return NotImplemented

    def bind(self, f):
        return f(self._value)


class NiladicMonad(Monad):

    def __repr__(self):
        return '{}()'.format(type(self).__qualname__)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return True
        else:
            return NotImplemented

    def bind(self, f):
        del f
        return self


class compose:

    """Kleisli composition operator, denoted >=>."""

    def __init__(self, f, g):
        self.f = f
        self.g = g

    def __repr__(self):
        return '{cls}({this.f!r}, {this.g!r})'.format(
            cls=type(self).__qualname__, this=self)

    def __call__(self, a):
        return self.f(a).bind(self.g)
