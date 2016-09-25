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

"""Test data constructors."""

import pytest

import mir.monads.data as data


class NullaryConstructor(metaclass=data.Constructor):
    arity = 0


class UnaryConstructor(metaclass=data.Constructor):
    arity = 1


@pytest.mark.parametrize('cls,args', [
    (NullaryConstructor, (1,)),
    (UnaryConstructor, ()),
])
def test_invalid_arguments(cls, args):
    with pytest.raises(TypeError):
        cls(*args)


@pytest.mark.parametrize('a,b,expected', [
    (UnaryConstructor(1), UnaryConstructor(1), True),
    (UnaryConstructor(1), (1,), False),
    (UnaryConstructor(1), UnaryConstructor(2), False),
])
def test_eq(a, b, expected):
    got = a == b
    assert got == expected
