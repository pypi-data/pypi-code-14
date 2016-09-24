import unittest

from uw_atg_wx import get_obs_from_uw_atg, get_obs

import unittest


class TestDispatcher(unittest.TestCase):

    def setUp(self):
        super().setUp()


    def test_get_obs_from_uw_atg(self):
        response = get_obs_from_uw_atg()
        self.assertGreater(len(list(response)), 1)
