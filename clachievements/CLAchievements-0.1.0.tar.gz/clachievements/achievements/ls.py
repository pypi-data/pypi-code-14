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

from . import Achievement, SimplePersistentDataAchievement
from ..testutils import test_lock, test_unlock

################################################################################

class AlwaysGiveCredit(SimplePersistentDataAchievement):
    """Run `ls` with names of `ls` authors as options."""

    title = "Always give credit"
    bin = ["ls"]
    icon = "copyleft.svg"
    default_data = set(["-David", "-Richard"])

    def __enter__(self):
        self.data -= set(self.command.argv)

    def __exit__(self, exc_type, exc_value, traceback):
        if len(self.data) == 0:
            self.unlock()

    @staticmethod
    @test_lock
    def test_one():
        """Test: iterate over commands that must not unlock this achievement."""
        yield "{bin.ls} -Richard"

    @staticmethod
    @test_unlock
    def test_single():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} -David -Richard"

    @staticmethod
    @test_unlock
    def test_separate():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} -David"
        yield "{bin.ls}"
        yield "{bin.ls} -Richard"

################################################################################

class WhenCreditIsDue(Achievement):
    """Run `ls` with names of `CLAchievements` author as options."""

    title = "When credit is due"
    bin = ["ls"]
    icon = "copyleft.svg"

    def __enter__(self):
        if "-Louis" in self.command.argv:
            self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} -Louis"

################################################################################

class ThereIsMoreThanOneWayToDoIt(Achievement):
    """Run `ls .`."""

    title = "There is more than one way to do it"
    bin = ["ls"]

    def __enter__(self):
        if self.command.argv[1:] == ["."]:
            self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} ."

################################################################################

class ListAllTheThings(Achievement):
    """Run `ls -R /` and wait for it to finish."""

    title = "List all the things!"
    bin = ["ls"]

    def __exit__(self, exc_type, exc_value, traceback):
        if (
                ("R" in self.command.short or "recursive" in self.command.long)
                and
                "/" in self.command.argv[1:]
            ):
            if isinstance(exc_value, SystemExit):
                if exc_value.code == 0:
                    self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} -Rd /"

################################################################################
