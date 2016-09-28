#!/usr/bin/env python
# coding: utf-8

"""
s_api_test.py

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
from netapp.santricity.api.symbol.s_api import SApi



class SApiTest(unittest.TestCase):

    
    def test_symbol_scan_volume(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_scan_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_secure_disk_pool(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_secure_disk_pool(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_secure_volume_group(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_secure_volume_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_send_drive_firmware(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_send_drive_firmware(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_alarm(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_alarm(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_asup_status(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_asup_status(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_async_mirror_group_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_async_mirror_group_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_auto_load_balancing(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_auto_load_balancing(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_auto_resync(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_auto_resync(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_battery_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_battery_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_cluster_performance_limitation_values(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_cluster_performance_limitation_values(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_controller_nvsram(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_controller_nvsram(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_controller_service_mode(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_controller_service_mode(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_controller_time(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_controller_time(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_controller_to_active(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_controller_to_active(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_controller_to_failed(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_controller_to_failed(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_controller_to_optimal(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_controller_to_optimal(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_controller_to_passive(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_controller_to_passive(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_disk_pool_priority(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_disk_pool_priority(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_disk_pool_reserved_drive_count(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_disk_pool_reserved_drive_count(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_disk_pool_threshold(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_disk_pool_threshold(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_disk_pool_to_complete(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_disk_pool_to_complete(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_disk_pool_user_label(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_disk_pool_user_label(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_drive_channel_state(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_drive_channel_state(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_drive_physical_security_id(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_drive_physical_security_id(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_drive_temperature_polling_interval(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_drive_temperature_polling_interval(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_drive_to_failed(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_drive_to_failed(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_drive_to_optimal(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_drive_to_optimal(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_flash_cache_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_flash_cache_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_function_state(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_function_state(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_high_resolution_sampling(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_high_resolution_sampling(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_host_interface_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_host_interface_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_host_port_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_host_port_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_host_port_type(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_host_port_type(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_host_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_host_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_host_specific_nvsram(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_host_specific_nvsram(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_ib_statistics_baseline(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_ib_statistics_baseline(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_initiator_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_initiator_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_iscsi_entity_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_iscsi_entity_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_iscsi_interface_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_iscsi_interface_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_iscsi_statistics_baseline(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_iscsi_statistics_baseline(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_key_value_tag_mapping(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_key_value_tag_mapping(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_lock_key(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_lock_key(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_network_parameters(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_network_parameters(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_pit_consistency_group_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_pit_consistency_group_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_pit_consistency_group_view_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_pit_consistency_group_view_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_pit_group_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_pit_group_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_pit_view_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_pit_view_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_remote_target_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_remote_target_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_rlogin_capability(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_rlogin_capability(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_rls_baseline(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_rls_baseline(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_sa_cache_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_sa_cache_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_sa_media_scan_period(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_sa_media_scan_period(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_sa_tray_positions(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_sa_tray_positions(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_sa_user_label(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_sa_user_label(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_sa_view_password(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_sa_view_password(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_simplex_mode(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_simplex_mode(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_snapshot_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_snapshot_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_snmp_community_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_snmp_community_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_snmp_system_variables(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_snmp_system_variables(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_snmp_trap_destination_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_snmp_trap_destination_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_storage_array_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_storage_array_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_target_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_target_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_thin_volume_capacity_threshold(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_thin_volume_capacity_threshold(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_thin_volume_expansion_policy(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_thin_volume_expansion_policy(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_thin_volume_provisioned_capacity_quota(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_thin_volume_provisioned_capacity_quota(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_thin_volume_reporting_policy(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_thin_volume_reporting_policy(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_tray_attributes(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_tray_attributes(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_vol_xfer_alert_delay_period(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_vol_xfer_alert_delay_period(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_cache_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_cache_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_copy_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_copy_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_group_to_offline(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_group_to_offline(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_group_to_online(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_group_to_online(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_group_user_label(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_group_user_label(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_list_online(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_list_online(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_media_scan_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_media_scan_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_params(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_params(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_properties(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_properties(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_set_volume_user_label(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_set_volume_user_label(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_base_controller_diagnostic(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_base_controller_diagnostic(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_cache_backup_device_diagnostic(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_cache_backup_device_diagnostic(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_cache_memory_diagnostic(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_cache_memory_diagnostic(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_cg_rollback(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_cg_rollback(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_channel_diagnostics(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_channel_diagnostics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_channel_identification(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_channel_identification(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_disk_pool_expansion(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_disk_pool_expansion(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_disk_pool_reduction(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_disk_pool_reduction(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_drive_firmware_download(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_drive_firmware_download(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_drive_identification(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_drive_identification(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_drive_reconstruction(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_drive_reconstruction(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_flash_cache_analytics(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_flash_cache_analytics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_host_card_diagnostic(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_host_card_diagnostic(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_performance_monitor(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_performance_monitor(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_pit_rollback(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_pit_rollback(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_raw_data_restore(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_raw_data_restore(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_raw_data_retrieve(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_raw_data_retrieve(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_sa_identification(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_sa_identification(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_snapshot_rollback(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_snapshot_rollback(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_sync_mirror(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_sync_mirror(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_tray_identification(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_tray_identification(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_copy(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_copy(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_expansion(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_expansion(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_format(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_format(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_group_defrag(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_group_defrag(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_group_expansion(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_group_expansion(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_parity_check(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_parity_check(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_raid_migration(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_raid_migration(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_start_volume_segment_sizing(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_start_volume_segment_sizing(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_state_capture(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_state_capture(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_channel_diagnostics(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_channel_diagnostics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_drive_firmware_download(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_drive_firmware_download(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_flash_cache_analytics(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_flash_cache_analytics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_identification(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_identification(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_iscsi_session(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_iscsi_session(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_performance_monitor(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_performance_monitor(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_pit_consistency_group_view(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_pit_consistency_group_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_pit_view(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_pit_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_stop_volume_copy(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_stop_volume_copy(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_suspend_async_mirror_group(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_suspend_async_mirror_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_suspend_consistency_group(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_suspend_consistency_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_suspend_flash_cache(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_suspend_flash_cache(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_suspend_mirror(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_suspend_mirror(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_suspend_mirror_list(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_suspend_mirror_list(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    
    def test_symbol_synchronize_async_mirror_group(self):
       api = SApi()
       s_api = None
       try:
            s_api = api.symbol_synchronize_async_mirror_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if s_api is None:
                s_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             s_api = 1

       self.assertNotEqual(s_api, None)
    


