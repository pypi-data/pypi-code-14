import unittest

from scaleway.apis.api_compute import ComputeAPI, REGIONS


class TestComputeAPI(unittest.TestCase):

    def test_set_region(self):
        self.assertEqual(ComputeAPI().base_url,
                         'https://cp-par1.scaleway.com/')
        self.assertEqual(ComputeAPI(region='par1').base_url,
                         'https://cp-par1.scaleway.com/')
        self.assertEqual(ComputeAPI(region='ams1').base_url,
                         'https://cp-ams1.scaleway.com/')
