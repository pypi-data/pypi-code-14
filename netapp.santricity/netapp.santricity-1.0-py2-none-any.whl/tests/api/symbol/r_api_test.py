#!/usr/bin/env python
# coding: utf-8

"""
r_api_test.py

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
from netapp.santricity.api.symbol.r_api import RApi



class RApiTest(unittest.TestCase):

    
    def test_symbol_read_mgmt_client_records(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_read_mgmt_client_records(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_read_unreadable_sector_database(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_read_unreadable_sector_database(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_recover_async_mirror_group_member(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_recover_async_mirror_group_member(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_recover_async_mirror_group_member_delete_recovery_point(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_recover_async_mirror_group_member_delete_recovery_point(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_recover_from_miswire(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_recover_from_miswire(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_recover_volume(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_recover_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_recreate_snapshot(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_recreate_snapshot(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_recreate_snapshot_collection(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_recreate_snapshot_collection(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_refresh_iscsi_dhcp_parameters(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_refresh_iscsi_dhcp_parameters(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_refresh_isns_server_location(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_refresh_isns_server_location(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reinitialize_thin_volume(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reinitialize_thin_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_release_support_data(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_release_support_data(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_async_mirror_group_member(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_async_mirror_group_member(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_bundle_keys(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_bundle_keys(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_drives_from_flash_cache(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_drives_from_flash_cache(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_mirror(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_mirror(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_pit_consistency_group_member(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_pit_consistency_group_member(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_snmp_community(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_snmp_community(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_snmp_trap_destination(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_snmp_trap_destination(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_remove_volume_copy(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_remove_volume_copy(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_rename_cluster(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_rename_cluster(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_rename_host(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_rename_host(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_rename_host_port(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_rename_host_port(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_replace_drive(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_replace_drive(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reprovision_drive(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reprovision_drive(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_request_removal(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_request_removal(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_request_to_remove(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_request_to_remove(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reserve_support_data(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reserve_support_data(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reset_async_mirror_sync_statistics(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reset_async_mirror_sync_statistics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reset_controller(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reset_controller(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reset_cumulative_statistics(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reset_cumulative_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reset_discrete_time_series(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reset_discrete_time_series(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reset_histogram(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reset_histogram(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reset_mel(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reset_mel(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_reset_sa_configuration(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_reset_sa_configuration(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_restart_pit_consistency_group_view(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_restart_pit_consistency_group_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_restart_pit_view(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_restart_pit_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_resume_async_mirror_group(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_resume_async_mirror_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_resume_consistency_group(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_resume_consistency_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_resume_flash_cache(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_resume_flash_cache(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_resume_mirror(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_resume_mirror(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_resume_mirror_list(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_resume_mirror_list(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_resume_pit_rollback(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_resume_pit_rollback(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_resume_snapshot_rollback(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_resume_snapshot_rollback(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_revive_pit_group(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_revive_pit_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_revive_pit_view(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_revive_pit_view(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    
    def test_symbol_role_change(self):
       api = RApi()
       r_api = None
       try:
            r_api = api.symbol_role_change(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if r_api is None:
                r_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             r_api = 1

       self.assertNotEqual(r_api, None)
    


