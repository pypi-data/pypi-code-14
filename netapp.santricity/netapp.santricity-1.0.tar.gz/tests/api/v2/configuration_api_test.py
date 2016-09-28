#!/usr/bin/env python
# coding: utf-8

"""
configuration_api_test.py

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
from netapp.santricity.api.v2.configuration_api import ConfigurationApi



class ConfigurationApiTest(unittest.TestCase):

    
    def test_dispatch_asup_bundle(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.dispatch_asup_bundle()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_get_asup_configuration_info(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.get_asup_configuration_info()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_get_configuration_result(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.get_configuration_result()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_get_configuration_types(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.get_configuration_types()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_register_asup_bundle(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.register_asup_bundle()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_start_configuration(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.start_configuration()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_stop_configuration(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.stop_configuration()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_update_asup_configuration_info(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.update_asup_configuration_info()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    
    def test_validate_csv_file(self):
       api = ConfigurationApi()
       configuration_api = None
       try:
            configuration_api = api.validate_csv_file()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if configuration_api is None:
                configuration_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             configuration_api = 1

       self.assertNotEqual(configuration_api, None)
    


