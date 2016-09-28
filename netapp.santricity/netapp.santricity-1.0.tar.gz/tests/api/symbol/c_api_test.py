#!/usr/bin/env python
# coding: utf-8

"""
c_api_test.py

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
from netapp.santricity.api.symbol.c_api import CApi



class CApiTest(unittest.TestCase):

    
    def test_symbol_calculate_dve_capacity(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_calculate_dve_capacity(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_async_mirror_group_role_change(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_async_mirror_group_role_change(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_base_controller_diagnostic(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_base_controller_diagnostic(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_cache_backup_device_diagnostic(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_cache_backup_device_diagnostic(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_cache_memory_diagnostic(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_cache_memory_diagnostic(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_database_recovery_mode(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_database_recovery_mode(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_evacuation(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_evacuation(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_host_card_diagnostic(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_host_card_diagnostic(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_import(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_import(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_pending_cgpit_creation(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_pending_cgpit_creation(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_pending_pit_creation(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_pending_pit_creation(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_pit_rollback(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_pit_rollback(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_raw_data_restore(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_raw_data_restore(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_raw_data_retrieve(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_raw_data_retrieve(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_cancel_snapshot_rollback(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_cancel_snapshot_rollback(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_change_async_mirror_group_role(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_change_async_mirror_group_role(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_change_mirror_write_mode(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_change_mirror_write_mode(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_change_synchronization_priority(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_change_synchronization_priority(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_async_mirror_group_fault_indication(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_async_mirror_group_fault_indication(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_async_mirror_group_member_fault_indication(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_async_mirror_group_member_fault_indication(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_ddc_needs_attention(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_ddc_needs_attention(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_dpl_core_dump_needs_retrieved(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_dpl_core_dump_needs_retrieved(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_drive_channel_statistics(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_drive_channel_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_persistent_registrations(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_persistent_registrations(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_sa_configuration(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_sa_configuration(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_sas_error_statistics(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_sas_error_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_soc_error_statistics(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_soc_error_statistics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_clear_unreadable_sectors(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_clear_unreadable_sectors(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_communication_check(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_communication_check(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_configure_pending_host(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_configure_pending_host(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_continue_raw_data_restore(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_continue_raw_data_restore(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_continue_raw_data_retrieve(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_continue_raw_data_retrieve(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_convert_read_only_pit_view_to_read_write(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_convert_read_only_pit_view_to_read_write(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_convert_snapshots_to_pit_groups(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_convert_snapshots_to_pit_groups(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_copy_drive_then_fail(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_copy_drive_then_fail(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_copy_drive_then_replace(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_copy_drive_then_replace(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_a_host_port(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_a_host_port(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_async_mirror_group(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_async_mirror_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_auto_config(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_auto_config(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_cgpit(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_cgpit(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_cluster(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_cluster(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_disk_pool(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_disk_pool(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_flash_cache(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_flash_cache(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_flash_cache_analytics(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_flash_cache_analytics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_host(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_host(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_host_port(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_host_port(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_initiator(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_initiator(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_key_value_tag(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_key_value_tag(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_lock_key(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_lock_key(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_lun_mapping(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_lun_mapping(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_metadata_volume(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_metadata_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_mirror(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_mirror(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_pit(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_pit(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_pit_consistency_group(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_pit_consistency_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_pit_consistency_group_view(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_pit_consistency_group_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_pit_group(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_pit_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_pit_view(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_pit_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_sa_port_group(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_sa_port_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_schedule_list(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_schedule_list(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_snapshot(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_snapshot(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_thin_volume(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_thin_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_volume(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_volume_group(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_volume_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_workload(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_workload(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    
    def test_symbol_create_workload_volume_mapping(self):
       api = CApi()
       c_api = None
       try:
            c_api = api.symbol_create_workload_volume_mapping(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if c_api is None:
                c_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             c_api = 1

       self.assertNotEqual(c_api, None)
    


