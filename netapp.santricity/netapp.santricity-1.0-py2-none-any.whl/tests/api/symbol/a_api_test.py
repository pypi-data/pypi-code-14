#!/usr/bin/env python
# coding: utf-8

"""
a_api_test.py

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
from netapp.santricity.api.symbol.a_api import AApi



class AApiTest(unittest.TestCase):

    
    def test_symbol_activate_discrete_time_series(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_activate_discrete_time_series(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_activate_fibre_channel_check_point_based_async_mirroring(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_activate_fibre_channel_check_point_based_async_mirroring(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_activate_histogram(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_activate_histogram(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_activate_host_port(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_activate_host_port(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_activate_initiator(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_activate_initiator(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_activate_mirroring(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_activate_mirroring(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_activate_staged_controller_firmware(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_activate_staged_controller_firmware(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_add_async_mirror_group_primary_member(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_add_async_mirror_group_primary_member(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_add_async_mirror_group_secondary_member(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_add_async_mirror_group_secondary_member(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_add_drives_to_flash_cache(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_add_drives_to_flash_cache(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_add_pending_host(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_add_pending_host(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_add_pit_consistency_group_member(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_add_pit_consistency_group_member(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_add_snmp_community(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_add_snmp_community(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_add_snmp_trap_destination(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_add_snmp_trap_destination(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_adopt_all_drives(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_adopt_all_drives(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_adopt_drive(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_adopt_drive(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_analyze_copy_on_write_repository(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_analyze_copy_on_write_repository(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_apply_bundle_key(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_apply_bundle_key(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_assign_disk_pool_ownership(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_assign_disk_pool_ownership(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_assign_drives_as_hot_spares(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_assign_drives_as_hot_spares(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_assign_specific_drives_as_hot_spares(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_assign_specific_drives_as_hot_spares(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_assign_volume_group_ownership(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_assign_volume_group_ownership(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_assign_volume_ownership(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_assign_volume_ownership(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_auto_assign_hot_spares(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_auto_assign_hot_spares(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_auto_load_balance_request(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_auto_load_balance_request(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    
    def test_symbol_auto_sa_configuration(self):
       api = AApi()
       a_api = None
       try:
            a_api = api.symbol_auto_sa_configuration(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if a_api is None:
                a_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             a_api = 1

       self.assertNotEqual(a_api, None)
    


