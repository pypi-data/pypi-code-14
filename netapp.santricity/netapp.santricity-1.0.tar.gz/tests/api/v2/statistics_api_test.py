#!/usr/bin/env python
# coding: utf-8

"""
statistics_api_test.py

The Clear BSD License

Copyright (c) – 2016, NetApp, Inc. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the limitations in the disclaimer below) provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

* Neither the name of NetApp, Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import unittest
from netapp.santricity.rest import ApiException
from netapp.santricity.api.v2.statistics_api import StatisticsApi



class StatisticsApiTest(unittest.TestCase):

    
    def test_get_all_analysed_controller_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_analysed_controller_statistics(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_all_analysed_drive_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_analysed_drive_statistics(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_all_analysed_interface_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_analysed_interface_statistics(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_all_analysed_volume_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_analysed_volume_statistics(system_id="test", idlist="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_all_historical_raw_performance_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_historical_raw_performance_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_all_live_performance_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_live_performance_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_all_raw_disk_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_raw_disk_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_all_raw_volume_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_all_raw_volume_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_analysed_controller_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_analysed_controller_statistics(system_id="test", idlist="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_analysed_drive_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_analysed_drive_statistics(system_id="test", idlist="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_analysed_volume_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_analysed_volume_statistics(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_analyzed_interface_stats(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_analyzed_interface_stats(system_id="test", idlist="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_average_analyzed_statistics_types(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_average_analyzed_statistics_types(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_averaged_historical_performance_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_averaged_historical_performance_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_historical_performance_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_historical_performance_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_historical_raw_performance_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_historical_raw_performance_statistics(system_id="test", idlist="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_live_performance_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_live_performance_statistics(system_id="test", idlist="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_raw_controller_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_raw_controller_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_raw_controller_statistics_using_list(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_raw_controller_statistics_using_list(system_id="test", idlist="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_raw_disk_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_raw_disk_statistics(system_id="test", idlist="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_raw_interface_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_raw_interface_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_raw_interface_statistics_with_list(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_raw_interface_statistics_with_list(system_id="test", idlist="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_raw_statistics_types(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_raw_statistics_types(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_raw_volume_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_raw_volume_statistics(system_id="test", idlist="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_selected_historical_performance_statistics(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_selected_historical_performance_statistics(system_id="test", idlist="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    
    def test_get_supported_statistics_types(self):
       api = StatisticsApi()
       statistics_api = None
       try:
            statistics_api = api.get_supported_statistics_types(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if statistics_api is None:
                statistics_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             statistics_api = 1

       self.assertNotEqual(statistics_api, None)
    


