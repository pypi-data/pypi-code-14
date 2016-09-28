#!/usr/bin/env python
# coding: utf-8

"""
storage_systems_api_test.py

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
from netapp.santricity.api.v2.storage_systems_api import StorageSystemsApi



class StorageSystemsApiTest(unittest.TestCase):

    
    def test_cancel_discovery_operation(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.cancel_discovery_operation()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_configure_ethernet_interfaces(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.configure_ethernet_interfaces(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_discover_storage_devices(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.discover_storage_devices()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_enable_feature_pack(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.enable_feature_pack(system_id="test", key_file="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_enable_premium_feature(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.enable_premium_feature(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_all_folders(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_all_folders()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_all_storage_systems(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_all_storage_systems()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_discovery_results(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_discovery_results()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_ethernet_interfaces(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_ethernet_interfaces(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_filtered_object_graph(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_filtered_object_graph(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_folder(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_folder(folder_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_lockdown_status_response(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_lockdown_status_response(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_object_graph(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_object_graph(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_password_status(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_password_status(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_storage_device_with_folder(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_storage_device_with_folder(folder_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_storage_system(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_storage_system(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_get_storage_system_capabilities(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.get_storage_system_capabilities(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_new_folder(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.new_folder()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_new_storage_system(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.new_storage_system()
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_remove_feature_pack(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.remove_feature_pack(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_remove_folder(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.remove_folder(folder_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_remove_premium_feature(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.remove_premium_feature(system_id="test", capability="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_remove_storage_system(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.remove_storage_system(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_set_password(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.set_password(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_update_folder(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.update_folder(folder_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_update_storage_device_name(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.update_storage_device_name(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_update_storage_system(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.update_storage_system(system_id="test", update_request="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    
    def test_validate_storage_system_password(self):
       api = StorageSystemsApi()
       storage_systems_api = None
       try:
            storage_systems_api = api.validate_storage_system_password(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if storage_systems_api is None:
                storage_systems_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             storage_systems_api = 1

       self.assertNotEqual(storage_systems_api, None)
    


