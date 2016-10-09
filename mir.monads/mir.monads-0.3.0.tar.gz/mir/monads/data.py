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

"""Data constructors for Python."""

import abc


class Constructor(abc.ABCMeta):

    """Metaclass for Haskell-like data constructors.

    Classes must define an arity class attribute.

    Very roughly speaking, equivalent to Haskell's:

        data SomeType a = SomeValue a

    Note that the hypothetical type constructor may take more arguments than
    the data constructor:

        data SomeType a = SomeValue
        data SomeType a b = SomeValue
        data SomeType a b = SomeValue a
        data SomeType a b c = SomeValue a
    """

    def __new__(meta, name, bases, dct):
        arity = int(dct.pop('arity'))
        dict_method = _dict_method(dct)

        @dict_method
        def __new__(cls, *values):
            if len(values) != arity:
                raise TypeError('__new__() takes %d arguments' % (arity,))
            return tuple.__new__(cls, values)

        @dict_method
        def __eq__(self, other):
            if isinstance(other, type(self)):
                return super(type(self), self).__eq__(other)
            else:
                return False

        bases += (tuple,)
        return super(Constructor, meta).__new__(meta, name, bases, dct)


def _dict_method(dct):
    """Decorator for adding methods to a dict."""
    def decorator(f):
        dct[f.__name__] = f
        return f
    return decorator
