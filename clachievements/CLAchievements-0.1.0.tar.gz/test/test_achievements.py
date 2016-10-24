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

"""Test that achievements are correctly unlocked."""

import os
import subprocess
import sys
import tempfile
import unittest

from clachievements.achievements import iter_achievements
from clachievements.db import TempDB
from clachievements.testutils import iter_test_methods
import clachievements

class SuppressStandard:
    """A context manager suppressing standard output and error

    Adapted from an original work:
    By jeremiahbuddha https://stackoverflow.com/users/772487/jeremiahbuddha
    Copied from http://stackoverflow.com/q/11130156
    Licensed under CC by-sa 3.0.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, output=True, error=True):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

        self.output = output
        self.error = error

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        if self.output:
            os.dup2(self.null_fds[0], 1)
        if self.error:
            os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        if self.output:
            os.dup2(self.save_fds[0], 1)
        if self.error:
            os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])

class ChangeTempDir(tempfile.TemporaryDirectory):
    """Context manager to change directory to a temporary one."""
    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._olddir = os.getcwd()

    def __enter__(self):
        os.chdir(super().__enter__())

    def __exit__(self, *args, **kwargs):
        os.chdir(self._olddir)
        return super().__exit__(*args, **kwargs)

class BinWrapper:
    """Wrap binaries using `python3 -m clachievements run BINARY`."""
    # pylint: disable=too-few-public-methods

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError("type object '{}' has no attribute '{}'".format(
                self.__class__.__name__,
                name,
                ))
        return "{python} -m clachievements run {bin}".format(
            python=sys.executable,
            bin=name,
            )


class TestAchievements(unittest.TestCase):
    """Test that achievements are correctly unlocked."""
    # pylint: disable=too-few-public-methods

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._oldpath = None

    @classmethod
    def setUpClass(cls):
        """Set environment variables"""
        os.environ["PYTHONPATH"] = ":".join((
            os.path.normpath(os.path.join(clachievements.__path__[0], "..")),
            os.environ.get("PYTHONPATH", ""),
            ))
        os.environ["CLA_TEST"] = ""

    def test_achievements(self):
        """Test that achievements are correctly unlocked."""
        for achievement in iter_achievements():
            unlocked = False
            for method in iter_test_methods(achievement):
                unlocked = unlocked or not method.test_lock
                with self.subTest(
                    msg="Testing achievement",
                    achievement=achievement.__name__,
                    method=method.__name__,
                    ):
                    with ChangeTempDir():
                        with TempDB() as database:
                            for command in method():
                                with SuppressStandard():
                                    subprocess.run(
                                        command.format(bin=BinWrapper()),
                                        shell=True,
                                        env=os.environ,
                                        )
                            self.assertEqual(database.is_locked(achievement), method.test_lock)
            if not unlocked:
                raise AssertionError(
                    "At least one test must unlock achievement '{}'.".format(achievement.__name__)
                    )
