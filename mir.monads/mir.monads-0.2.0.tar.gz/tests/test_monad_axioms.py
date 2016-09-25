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

"""Test that monads satisfy the monad axioms."""

import pytest

import mir.monads.maybe as maybe


def add_one(a):
    return a + 1


def times_two(a):
    return a * 2


@pytest.mark.parametrize('unit,f,a', [
    (maybe.Just, maybe.monadic(add_one), 1),
])
def test_bind_left_identity(unit, f, a):
    """return a >>= f ≡ f a

    return >=> g ≡ g
    """
    assert (unit(a) >> f) == f(a)


@pytest.mark.parametrize('m,unit', [
    (maybe.Just(1), maybe.Just),
])
def test_bind_right_identity(m, unit):
    """m >>= return ≡ m

    f >=> return ≡ f
    """
    assert (m >> unit) == m


@pytest.mark.parametrize('m,f,g', [
    (maybe.Just(1), maybe.monadic(add_one), maybe.monadic(times_two)),
])
def test_bind_associativity(m, f, g):
    r"""(m >>= f) >>= g ≡ m >>= (\x -> f x >>= g)

    (f >=> g) >=> h ≡ f >=> (g >=> h)
    """
    assert (m >> f >> g) == (m >> (lambda x: f(x) >> g))
