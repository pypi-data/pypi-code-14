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

"""Tests for mir.monads.fun module."""

import pytest

import mir.monads.fun as fun


def test_currying_when_unbound_params():
    function = fun.curry(lambda a, b: 1)  # pragma: no branch
    got = function(1)
    assert callable(got)


def test_calling_when_no_params():
    function = fun.curry(lambda a: 1)
    got = function(1)
    assert got == 1


def test_calling_curried_function():
    function = fun.curry(lambda a, b: 1)
    got = function(1)(2)
    assert got == 1


def test_mul_composition():
    f = fun.curry(lambda a: a + 1)
    g = fun.curry(lambda a: a * 2)
    assert (f * g)(1) == 3


@pytest.mark.parametrize(  # pragma: no branch
    'f,args,expected', [
        (lambda: 1, (), True),
        (lambda a: 1, (), False),
        (lambda a: 1, (1,), True),
        (lambda a, b: 1, (1,), False),
    ])
def test__is_fully_bound(f, args, expected):
    got = fun._is_fully_bound(f, args)
    assert bool(got) == expected
