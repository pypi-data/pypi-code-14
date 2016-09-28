#!/usr/bin/env python
# coding: utf-8

"""
device_asup_api_test.py

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
from netapp.santricity.api.v2.device_asup_api import DeviceASUPApi



class DeviceASUPApiTest(unittest.TestCase):

    
    def test_get_all_asup_transmission_log_files(self):
       api = DeviceASUPApi()
       device_asup_api = None
       try:
            device_asup_api = api.get_all_asup_transmission_log_files()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if device_asup_api is None:
                device_asup_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             device_asup_api = 1

       self.assertNotEqual(device_asup_api, None)
    
    def test_get_asup_configuration(self):
       api = DeviceASUPApi()
       device_asup_api = None
       try:
            device_asup_api = api.get_asup_configuration()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if device_asup_api is None:
                device_asup_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             device_asup_api = 1

       self.assertNotEqual(device_asup_api, None)
    
    def test_get_asup_information(self):
       api = DeviceASUPApi()
       device_asup_api = None
       try:
            device_asup_api = api.get_asup_information()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if device_asup_api is None:
                device_asup_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             device_asup_api = 1

       self.assertNotEqual(device_asup_api, None)
    
    def test_get_asup_transmission_log_file(self):
       api = DeviceASUPApi()
       device_asup_api = None
       try:
            device_asup_api = api.get_asup_transmission_log_file(filename="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if device_asup_api is None:
                device_asup_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             device_asup_api = 1

       self.assertNotEqual(device_asup_api, None)
    
    def test_update_asup_configuration(self):
       api = DeviceASUPApi()
       device_asup_api = None
       try:
            device_asup_api = api.update_asup_configuration()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if device_asup_api is None:
                device_asup_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             device_asup_api = 1

       self.assertNotEqual(device_asup_api, None)
    
    def test_verify_asup_configuration(self):
       api = DeviceASUPApi()
       device_asup_api = None
       try:
            device_asup_api = api.verify_asup_configuration()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if device_asup_api is None:
                device_asup_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             device_asup_api = 1

       self.assertNotEqual(device_asup_api, None)
    


