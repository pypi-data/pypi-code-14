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

"""Maybe monad.

Useful for replacing the awful None type in Python.
"""

import functools

import mir.monads.abc as monads_abc
import mir.monads.data as data


class Maybe(monads_abc.Monad):
    """Maybe monad supertype"""


class Just(Maybe, metaclass=data.Constructor):

    """Just monad"""

    arity = 1

    def fmap(self, f):
        value, = self
        try:
            new_value = f(value)
        except Exception:
            new_value = None
        if new_value is None:
            return Nothing()
        else:
            return Just(new_value)

    def apply(self, other):
        value, = self
        return other.fmap(value)

    def bind(self, f):
        value, = self
        return f(value)


class Nothing(Maybe, metaclass=data.Constructor):

    """Nothing monad"""

    arity = 0

    def fmap(self, f):
        return Nothing()

    def apply(self, other):
        return Nothing()

    def bind(self, f):
        return Nothing()


def monadic(f):
    """Decorate a unary function to return a Maybe type."""
    @functools.wraps(f)
    def wrapped(a):
        try:
            b = f(a)
        except Exception:
            b = None
        if b is None:
            return Nothing()
        else:
            return Just(b)
    return wrapped
