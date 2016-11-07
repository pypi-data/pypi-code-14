u"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
import sys
import unittest
from toktokkie.utils.iconizing.procedures.GnomeProcedure import GnomeProcedure


class GnomeProcedureUnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_applicability(self):

        if sys.platform == u"linux":
            try:
                self.assertEqual(os.environ[u"DESKTOP_SESSION"] in [u"cinnamon", u"gnome"], GnomeProcedure.is_applicable())
            except KeyError:
                self.assertFalse(GnomeProcedure.is_applicable())

    def test(self):
        pass
