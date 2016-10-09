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

"""Tests for Maybe Monad."""

import mir.monads.maybe as maybe


@maybe.monadic
def invert(a):
    return 1 / a


def test_bind():
    assert maybe.Just(2) >> invert == maybe.Just(0.5)


def test_bind_nothing():
    assert maybe.Just(0) >> invert >> invert == maybe.Nothing()


def test_fmap_just():
    assert maybe.Just(1).fmap(lambda x: x + 1) == maybe.Just(2)


def test_fmap_just_none():
    assert maybe.Just(1).fmap(lambda x: None) == maybe.Nothing()


def test_fmap_just_exception():
    assert maybe.Just(1).fmap(lambda x: 1 + '') == maybe.Nothing()


def test_fmap_nothing():
    assert maybe.Nothing().fmap(lambda x: x + 1) == maybe.Nothing() # pragma: no branch


def test_apply_just():
    assert maybe.Just(lambda x: x + 1).apply(maybe.Just(1)) == maybe.Just(2)


def test_apply_nothing():
    assert maybe.Nothing().apply(maybe.Just(1)) == maybe.Nothing()
