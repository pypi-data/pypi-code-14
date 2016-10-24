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

"""Achievements only looking at command line options."""

import os

from . import Achievement
from ..testutils import test_unlock, test_lock

################################################################################

class SoundOfSilence(Achievement):
    """Run a command with both "--verbose" and "--quiet" options."""

    title = "Sound Of Silence"
    bin = ["chgrp", "chmod", "chown", "head", "readlink", "tail"]
    options = {
        "chgrp": (
            (set(["f"]), set(["silent", "quiet"])),
            (set(["v"]), set(["verbose"])),
            ),
        "chmod": (
            (set(["f"]), set(["silent", "quiet"])),
            (set(["v"]), set(["verbose"])),
            ),
        "chown": (
            (set(["f"]), set(["silent", "quiet"])),
            (set(["v"]), set(["verbose"])),
            ),
        "head": (
            (set(["q"]), set(["silent", "quiet"])),
            (set(["v"]), set(["verbose"])),
            ),
        "readlink": (
            (set(["q", "s"]), set(["silent", "quiet"])),
            (set(["v"]), set(["verbose"])),
            ),
        "tail": (
            (set(["q"]), set(["silent", "quiet"])),
            (set(["v"]), set(["verbose"])),
            ),
        }

    def __enter__(self):
        if (
                (
                    (self.options[self.command.bin][0][0] & self.command.short.keys())
                    |
                    (self.options[self.command.bin][0][1] & self.command.long.keys())
                ) and (
                    (self.options[self.command.bin][1][0] & self.command.short.keys())
                    |
                    (self.options[self.command.bin][1][1] & self.command.long.keys())
                )
            ):
            self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        yield "{bin.chmod} -f --verbose 777 foo"

    @staticmethod
    @test_unlock
    def test_unlock2():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        yield "{bin.head} -q -v foo"

    @staticmethod
    @test_unlock
    def test_unlock3():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch foo"
        yield "{bin.tail} --verbose --quiet foo"

################################################################################

def which(binary):
    """Return the full path of binary.

    More or less equivalent to the `which` shell command.

    Return ``None`` string if command cannot be found.
    """
    if binary.startswith("."):
        return os.path.abspath(binary)
    for path in os.environ["PATH"].split(":"):
        if os.path.exists(os.path.join(path, binary)):
            return os.path.abspath(os.path.join(path, binary))
    return None

class SelfReference(Achievement):
    """Run a binary on itself."""

    title = "Self reference"

    def __enter__(self):
        if which(self.command.argv[0]) in (os.path.abspath(arg) for arg in self.command.positional):
            self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} " + which("ls")

    @staticmethod
    @test_lock
    def test_lock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "touch ls"
        yield "{bin.ls} ls"

################################################################################

class KnowItAll(Achievement):
    """Run a command with 10 options or more, without errors."""

    title = "Know it all"

    def __exit__(self, exc_type, exc_value, traceback):
        if isinstance(exc_value, SystemExit):
            if exc_value.code == 0:
                if len(self.command.short) + len(self.command.long) >= 10:
                    self.unlock()

    @staticmethod
    @test_unlock
    def test_unlock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} -abcdfghiklmnop"

    @staticmethod
    @test_lock
    def test_lock1():
        """Test: iterate over commands that must unlock this achievement."""
        yield "{bin.ls} -abcdfghiklmnop --doesnotexist"
