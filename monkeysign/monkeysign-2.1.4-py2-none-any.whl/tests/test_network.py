#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright (C) 2012-2013 Antoine Beaupré <anarcat@orangeseeds.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests that hit the network.

Those tests are in a separate file to allow the base set of tests to
be ran without internet access.
"""

import unittest

import os
import sys
sys.path.insert(0, os.path.dirname(__file__) + '/../..')

from monkeysign.gpg import TempKeyring
from test_lib import TestTimeLimit, AlarmException, find_test_file
import test_ui


def skipUnlessNetwork():
    """add a knob to disable network tests

    to disable network tests, use PYTEST_USENETWORK=no. by default, it
    is assumed there is network access.

    this is mainly to deal with Debian packages that are built in
    network-less chroots. unfortunately, there is no standard
    environment in dpkg-buildpackage or ./debian/rules binary that we
    can rely on to disable tests, so we revert to a custom variable
    that can hopefully make it up to the pybuild toolchain

    I looked at DEB_BUILD_OPTIONS=network, but that is not standard
    and only mentionned once here:

    https://lists.debian.org/debian-devel/2009/09/msg00992.html

    DEB_BUILD_OPTIONS is also not set by default, so it's not a good
    way to detect Debian package builds

    pbuilder uses USENETWORK=no/yes, schroot uses UNSHARE_NET, but
    those are not standard either, see:

    https://github.com/spotify/dh-virtualenv/issues/77
    https://github.com/codelibre-net/schroot/blob/2e3d015a759d2b5106e851af34c8d5974d84f18e/lib/schroot/chroot/facet/unshare.cc
    """

    if ('PYTEST_USENETWORK' in os.environ
       and 'no' in os.environ.get('PYTEST_USENETWORK', '')):
        return unittest.skip('network tests disabled (PYTEST_USENETWORK=no)')
    else:
        return lambda func: func


@skipUnlessNetwork()
class TestGpgNetwork(TestTimeLimit):

    """Separate test cases for functions that hit the network

each test needs to run under a specific timeout so we don't wait on
the network forever"""

    def setUp(self):
        self.gpg = TempKeyring()
        self.gpg.context.set_option('keyserver', 'pool.sks-keyservers.net')
        TestTimeLimit.setUp(self)

    def test_fetch_keys(self):
        """test key fetching from keyservers"""
        try:
            self.assertTrue(self.gpg.fetch_keys('4023702F'))
        except AlarmException:
            raise unittest.case._ExpectedFailure(sys.exc_info())

    def test_special_key(self):
        """test a key that sign_key had trouble with"""
        self.assertTrue(self.gpg.import_data(open(find_test_file('96F47C6A.asc')).read()))
        self.assertTrue(self.gpg.import_data(open(find_test_file('96F47C6A-secret.asc')).read()))
        try:
            self.assertTrue(self.gpg.fetch_keys('3CCDBB7355D1758F549354D20B123309D3366755'))
        except AlarmException:
            raise unittest.case._ExpectedFailure(sys.exc_info())
        self.assertTrue(self.gpg.sign_key('3CCDBB7355D1758F549354D20B123309D3366755', True))

    def tearDown(self):
        TestTimeLimit.tearDown(self)
        del self.gpg


@skipUnlessNetwork()
class KeyserverTests(test_ui.BaseTestCase):
    args = ['--keyserver', 'pool.sks-keyservers.net']
    pattern = '7B75921E'

    def test_find_key(self):
        """this should find the key on the keyservers"""
        self.ui.find_key()

if __name__ == '__main__':
    unittest.main()
