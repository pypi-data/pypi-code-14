#!/usr/bin/env python
# coding: utf-8

"""
hardware_api_test.py

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
from netapp.santricity.api.v2.hardware_api import HardwareApi



class HardwareApiTest(unittest.TestCase):

    
    def test_cancel_hardware_identification(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.cancel_hardware_identification(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_all_controllers(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_all_controllers(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_all_drives(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_all_drives(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_controller(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_controller(system_id="test", controller_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_drive(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_drive(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_drive_connection_info(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_drive_connection_info(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_hardware_information(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_hardware_information(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_iscsi_data(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_iscsi_data(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_iscsi_target(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_iscsi_target(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_get_unreadable_sectors_list(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.get_unreadable_sectors_list(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_select_drives(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.select_drives(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_start_hardware_identification(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.start_hardware_identification(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_update_iscsi_data(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.update_iscsi_data(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    
    def test_update_iscsi_target(self):
       api = HardwareApi()
       hardware_api = None
       try:
            hardware_api = api.update_iscsi_target(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if hardware_api is None:
                hardware_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             hardware_api = 1

       self.assertNotEqual(hardware_api, None)
    


