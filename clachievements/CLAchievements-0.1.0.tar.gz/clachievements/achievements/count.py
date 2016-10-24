# Command Line Achievements
# Copyright 2016 Louis Paternault
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Achievements related exclusively to `ls`."""

from . import SimplePersistentDataAchievement
from ..testutils import test_lock, test_unlock

################################################################################

class CoinFlipping(SimplePersistentDataAchievement):
    """Use `head` and `tail` at least 100 times (combined)."""

    title = "Coin flipping"
    bin = ["head", "tail"]
    default_data = {'head': 0, 'tail': 0}

    def __enter__(self):
        copy = self.data
        copy[self.command.bin] += 1
        self.data = copy

    def __exit__(self, exc_type, exc_value, traceback):
        if self.data['head'] + self.data['tail'] >= 100:
            self.unlock()

    @staticmethod
    @test_unlock
    def test_head():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        for _ in range(100):
            yield "{bin.head} foo"

    @staticmethod
    @test_unlock
    def test_tail():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        for _ in range(100):
            yield "{bin.tail} foo"

    @staticmethod
    @test_unlock
    def test_combined():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        for _ in range(50):
            yield "{bin.head} foo"
            yield "{bin.tail} foo"

    @staticmethod
    @test_lock
    def test_lock1():
        """Test: iterate over commands that must not unlock this achievement."""
        yield "touch foo"
        for _ in range(49):
            yield "{bin.head} foo"
            yield "{bin.tail} foo"

################################################################################

class SomethingToHide(SimplePersistentDataAchievement):
    """Use `shred` more than 10 times."""

    title = "Something to hide"
    bin = ["shred"]
    default_data = 0

    def __enter__(self):
        self.data += 1
        if self.data >= 10:
            self.unlock()

    @staticmethod
    @test_unlock
    def test_head():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        for _ in range(10):
            yield "{bin.shred} -n1 foo"

################################################################################

class Lost(SimplePersistentDataAchievement):
    """Use `pwd` more than 50 times."""

    title = "Lost"
    bin = ["pwd"]
    default_data = 0

    def __enter__(self):
        self.data += 1
        if self.data >= 50:
            self.unlock()

    @staticmethod
    @test_unlock
    def test_head():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        for _ in range(50):
            yield "{bin.pwd}"

################################################################################

class Philosopher(SimplePersistentDataAchievement):
    """Use `whoami` more than 10 times."""

    title = "Philosopher"
    bin = ["whoami"]
    default_data = 0

    def __enter__(self):
        self.data += 1
        if self.data >= 10:
            self.unlock()

    @staticmethod
    @test_unlock
    def test_head():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        for _ in range(10):
            yield "{bin.whoami}"

################################################################################

class Liar(SimplePersistentDataAchievement):
    """Use `true` and `false`."""

    title = "Liar"
    bin = ["true", "false"]
    default_data = set(["true", "false"])

    @staticmethod
    @test_unlock
    def test_unlock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.true}"
        yield "{bin.false}"

    def __enter__(self):
        self.data -= set([self.command.bin])
        if len(self.data) == 0:
            self.unlock()
