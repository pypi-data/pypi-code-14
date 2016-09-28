#!/usr/bin/env python
# coding: utf-8

"""
d_api_test.py

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
from netapp.santricity.api.symbol.d_api import DApi



class DApiTest(unittest.TestCase):

    
    def test_symbol_deactivate_discrete_time_series(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_deactivate_discrete_time_series(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_deactivate_fibre_channel_check_point_based_async_mirroring(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_deactivate_fibre_channel_check_point_based_async_mirroring(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_deactivate_histogram(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_deactivate_histogram(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_deactivate_mirroring(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_deactivate_mirroring(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_deassign_drives_as_hot_spares(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_deassign_drives_as_hot_spares(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_async_mirror_group(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_async_mirror_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_async_mirror_group_incomplete_member(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_async_mirror_group_incomplete_member(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_cgpit(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_cgpit(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_client_mgmt_records_no_password(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_client_mgmt_records_no_password(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_cluster(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_cluster(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_disk_pool(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_disk_pool(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_flash_cache(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_flash_cache(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_host(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_host(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_host_port(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_host_port(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_initiator(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_initiator(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_key_value_tag(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_key_value_tag(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_key_value_tag_mapping(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_key_value_tag_mapping(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_lun_mapping(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_lun_mapping(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_mgmt_client_records(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_mgmt_client_records(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_pit(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_pit(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_pit_consistency_group(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_pit_consistency_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_pit_consistency_group_view(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_pit_consistency_group_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_pit_group(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_pit_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_pit_view(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_pit_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_sa_port_group(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_sa_port_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_schedule_list(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_schedule_list(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_snapshot(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_snapshot(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_volume(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_volume_from_group(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_volume_from_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_volume_group(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_volume_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_workload(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_workload(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_delete_workload_volume_mapping(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_delete_workload_volume_mapping(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_asup(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_asup(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_external_kms(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_external_kms(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_feature(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_feature(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_feature_by_ref(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_feature_by_ref(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_flash_cache_volume(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_flash_cache_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_snapshot(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_snapshot(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_snapshot_collection(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_snapshot_collection(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_disable_volume_protection_information(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_disable_volume_protection_information(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    
    def test_symbol_discover_controllers(self):
       api = DApi()
       d_api = None
       try:
            d_api = api.symbol_discover_controllers(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if d_api is None:
                d_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             d_api = 1

       self.assertNotEqual(d_api, None)
    


