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

"""Test the `Command` class"""

import unittest

from multidict import MultiDict

from clachievements.run import Command

class TestCommand(unittest.TestCase):
    """Test the Command class."""

    def test_empty(self):
        """Test with an empty command."""
        command = Command(["/usr/bin/ls"])
        self.assertEqual(command.short, MultiDict())
        self.assertEqual(command.long, MultiDict())
        self.assertEqual(command.positional, list())
        self.assertEqual(command.argv, ["/usr/bin/ls"])
        self.assertEqual(command.bin, "ls")

    def test_full(self):
        """Test with many arguments."""
        line = "/usr/bin/ls --long1=foo --long2=bar --long1 --long2=baz pos1 pos2 pos3 -short -arguments".split() # pylint: disable=line-too-long
        command = Command(line)
        self.assertEqual(
            command.long,
            MultiDict([
                ("long1", "foo"),
                ("long2", "bar"),
                ("long1", None),
                ("long2", "baz"),
                ]))
        self.assertEqual(
            command.short,
            MultiDict([
                ("s", None),
                ("h", None),
                ("o", None),
                ("r", None),
                ("t", None),
                ("a", None),
                ("r", None),
                ("g", None),
                ("u", None),
                ("m", None),
                ("e", None),
                ("n", None),
                ("t", None),
                ("s", None),
                ]))
        self.assertEqual(
            command.positional,
            ["pos1", "pos2", "pos3"],
            )
        self.assertEqual(
            command.argv,
            line,
            )
        self.assertEqual(
            command.bin,
            "ls",
            )
