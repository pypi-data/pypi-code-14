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

"""Functional programming goodies."""

import inspect


class curry:

    """Decorator to enable currying for a function.

    Calling a curry-able function will either return a partial function or call
    the function and return its result.  The function will only be called if it
    has no unbound parameters.

    Currying a function with keyword-only parameters is an error.

    Default parameter values are effectively ignored.
    """

    def __init__(self, func, args=()):
        self._func = func
        self._args = args

    def __repr__(self):
       return '{cls}({this._func!r}, {this._args!r})'.format(
           cls=type(self).__qualname__,
           this=self)

    def __call__(self, *args):
        func = self._func
        new_args = self._args + args
        if _is_fully_bound(func, new_args):
            return func(*new_args)
        else:
            return curry(self._func, new_args)

    def __mul__(self, other):
        return composition(self, other)


def _is_fully_bound(f, args):
    """Return True if the given arguments bind all of the function's parameters."""
    sig = inspect.signature(f)
    bound_args = sig.bind_partial(*args)
    return len(sig.parameters) == len(bound_args.arguments)


class composition:

    """Function composition."""

    def __init__(self, a, b):
        assert callable(a), 'Cannot compose non-callable %r' % (a,)
        assert callable(b), 'Cannot compose non-callable %r' % (b,)
        self._a = a
        self._b = b

    def __repr__(self):
        return '{cls}({this._a!r}, {this._b!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def __call__(self, *args, **kwargs):
        return self._a(self._b(*args, **kwargs))
