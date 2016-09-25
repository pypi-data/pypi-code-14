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

"""Tests for Identity Monad."""

from mir.monads.id import Identity


def test_fmap():
    assert Identity(1).fmap(lambda x: x + 1) == Identity(2)


def test_apply():
    assert Identity(lambda x: x + 1).apply(Identity(1)) == Identity(2)


def test_bind():
    assert Identity(1) >> (lambda x: Identity(x + 1)) == Identity(2)
