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

"""Identity monad.

Useful for doing something like Clojure's threading operator using fmap().
"""

import functools

import mir.monads.abc as monads_abc
import mir.monads.data as data


class Identity(monads_abc.Monad, metaclass=data.Constructor):

    """Identity monad."""

    arity = 1

    def fmap(self, f):
        value, = self
        return Identity(f(value))

    def apply(self, other):
        value, = self
        return other.fmap(value)

    def bind(self, f):
        value, = self
        return f(value)
