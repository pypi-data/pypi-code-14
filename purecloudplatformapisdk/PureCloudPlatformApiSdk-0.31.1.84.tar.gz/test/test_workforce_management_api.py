# coding: utf-8

"""
Copyright 2016 SmartBear Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   ref: https://github.com/swagger-api/swagger-codegen
"""

from __future__ import absolute_import

import os
import sys
import unittest

import swagger_client
from swagger_client.rest import ApiException
from swagger_client.apis.workforce_management_api import WorkforceManagementApi


class TestWorkforceManagementApi(unittest.TestCase):
    """ WorkforceManagementApi unit test stubs """

    def setUp(self):
        self.api = swagger_client.apis.workforce_management_api.WorkforceManagementApi()

    def tearDown(self):
        pass

    def test_delete_longtermforecasts_forecast_id(self):
        """
        Test case for delete_longtermforecasts_forecast_id

        Delete a forecast
        """
        pass

    def test_delete_longtermforecasts_forecast_id_modifications_forecastmodification_id(self):
        """
        Test case for delete_longtermforecasts_forecast_id_modifications_forecastmodification_id

        Delete a forecast modification
        """
        pass

    def test_get_adherence(self):
        """
        Test case for get_adherence

        Get a list of UserScheduleAdherence records for the requested users
        """
        pass

    def test_get_longtermforecasts_forecast_id(self):
        """
        Test case for get_longtermforecasts_forecast_id

        Get forecast
        """
        pass

    def test_get_longtermforecasts_forecast_id_modifications(self):
        """
        Test case for get_longtermforecasts_forecast_id_modifications

        Get forecast Modifications
        """
        pass

    def test_post_longtermforecasts(self):
        """
        Test case for post_longtermforecasts

        Create a forecast
        """
        pass

    def test_post_longtermforecasts_forecast_id_modifications(self):
        """
        Test case for post_longtermforecasts_forecast_id_modifications

        Create a forecast modification
        """
        pass

    def test_post_longtermforecasts_search(self):
        """
        Test case for post_longtermforecasts_search

        Search forecasts
        """
        pass

    def test_put_longtermforecasts_forecast_id_modifications(self):
        """
        Test case for put_longtermforecasts_forecast_id_modifications

        Update a forecast modification
        """
        pass


if __name__ == '__main__':
    unittest.main()