u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via the XDCC
    protocol via file serving bots on IRC networks.

    xdcc_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    xdcc_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xdcc_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import os
import unittest
from xdcc_dl.pack_searchers.PackSearcher import PackSearcher


class UnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_intel_haruhichan(self):
        results = PackSearcher([u"intel_haruhichan"]).search(u"Gin.txt")

        self.assertEqual(results[0].get_packnumber(), 1)
        self.assertEqual(results[0].get_server().get_address(), u"irc.rizon.net")
        self.assertEqual(results[0].get_filepath(), os.path.join(os.getcwdu(), results[0].get_filename()))
        self.assertEqual(results[0].get_filename(), u"Gin.txt")
        self.assertEqual(results[0].get_bot(), u"Ginpachi-Sensei")
        self.assertEqual(len(results), 1)

    def test_nibl(self):
        results = PackSearcher([u"nibl"]).search(u"Gin.txt")

        self.assertEqual(results[0].get_packnumber(), 1)
        self.assertEqual(results[0].get_server().get_address(), u"irc.rizon.net")
        self.assertEqual(results[0].get_filepath(), os.path.join(os.getcwdu(), results[0].get_filename()))
        self.assertEqual(results[0].get_filename(), u"Gin.txt")
        self.assertEqual(results[0].get_bot(), u"Ginpachi-Sensei")
        self.assertEqual(len(results), 1)

    def test_ixirc(self):
        results = PackSearcher([u"ixirc"]).search(u"Gin.txt")

        self.assertEqual(results[0].get_packnumber(), 1)
        self.assertEqual(results[0].get_server().get_address(), u"irc.abjects.net")
        self.assertEqual(results[0].get_filepath(), os.path.join(os.getcwdu(), results[0].get_filename()))
        self.assertEqual(results[0].get_filename(), u"Gin.txt")
        self.assertEqual(results[0].get_bot(), u"Beast-Gin-Anime")
        self.assertEqual(len(results), 1)

    def test_all(self):

        results = PackSearcher().search(u"Gin.txt")
        self.assertEqual(len(results), len(PackSearcher.get_available_pack_searchers()))
