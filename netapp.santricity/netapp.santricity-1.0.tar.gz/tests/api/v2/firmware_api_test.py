#!/usr/bin/env python
# coding: utf-8

"""
firmware_api_test.py

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
from netapp.santricity.api.v2.firmware_api import FirmwareApi



class FirmwareApiTest(unittest.TestCase):

    
    def test_activate_staged_controller_firmware(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.activate_staged_controller_firmware(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_activate_staged_firmware(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.activate_staged_firmware()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_begin_compatibility_check(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.begin_compatibility_check()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_cancel_compatibility_check(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.cancel_compatibility_check()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_cancel_health_check(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.cancel_health_check()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_check_embedded_firmware_bundle_compatibility(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.check_embedded_firmware_bundle_compatibility(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_check_embedded_nvsram_compatibility(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.check_embedded_nvsram_compatibility(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_clear_staged_firmware(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.clear_staged_firmware(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_all_firmware_files(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_all_firmware_files()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_compatibility_check_results(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_compatibility_check_results()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_controller_firmware_upgrade_status(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_controller_firmware_upgrade_status(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_embedded_firmware_information(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_embedded_firmware_information()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_firmware_details(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_firmware_details(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_firmware_file(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_firmware_file(filename="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_health_check_status(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_health_check_status()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_iom_service_information(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_iom_service_information()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_staged_controller_firmware_details(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_staged_controller_firmware_details(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_get_staged_firmware_details(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.get_staged_firmware_details(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_remove_firmware_file(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.remove_firmware_file(filename="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_remove_staged_firmware(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.remove_staged_firmware(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_start_controller_firmware_upgrade(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.start_controller_firmware_upgrade(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_start_health_check(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.start_health_check()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_update_iom_service_information(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.update_iom_service_information()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_upload_embedded_firmware_file(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.upload_embedded_firmware_file()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_upload_firmware_file(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.upload_firmware_file(firmware_file="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    
    def test_upload_nvsram_file(self):
       api = FirmwareApi()
       firmware_api = None
       try:
            firmware_api = api.upload_nvsram_file(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if firmware_api is None:
                firmware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             firmware_api = 1

       self.assertNotEqual(firmware_api, None)
    


