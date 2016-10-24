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

"""Achievements related to file system."""

import os

from . import Achievement, SimplePersistentDataAchievement
from ..testutils import test_unlock
from ..db import db_path

################################################################################

class Maker(SimplePersistentDataAchievement):
    """Use all commands starting with `mk`."""

    title = "Maker"
    bin = ["mkdir", "mkfifo", "mknod", "mktemp"]
    default_data = set(["mkdir", "mkfifo", "mknod", "mktemp"])

    def __enter__(self):
        self.data -= set([self.command.bin])
        if len(self.data) == 0:
            self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.mkdir foo}"
        yield "{bin.mkfifo bar}"
        yield "{bin.mknod}"
        yield "{bin.mktemp}"

################################################################################

class H4x0r(Achievement):
    """Mess with CLA data files."""
    title = "H4x0r"

    def __enter__(self):
        if os.path.abspath(db_path()) in (os.path.abspath(arg) for arg in self.command.positional):
            self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} " + db_path()

################################################################################
