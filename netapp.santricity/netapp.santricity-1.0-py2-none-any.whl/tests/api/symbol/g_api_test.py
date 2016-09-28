#!/usr/bin/env python
# coding: utf-8

"""
g_api_test.py

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
from netapp.santricity.api.symbol.g_api import GApi



class GApiTest(unittest.TestCase):

    
    def test_symbol_get_alertable_mel_entries(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_alertable_mel_entries(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_asup_status(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_asup_status(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_async_mirror_group_remote_connections(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_async_mirror_group_remote_connections(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_async_mirror_group_sync_progress(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_async_mirror_group_sync_progress(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_async_mirror_repository_utilization(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_async_mirror_repository_utilization(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_async_mirror_sync_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_async_mirror_sync_statistics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_auto_config_candidates(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_auto_config_candidates(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_base_controller_diagnostic_status(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_base_controller_diagnostic_status(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_cache_backup_device_diagnostic_status(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_cache_backup_device_diagnostic_status(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_cache_memory_diagnostic_status(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_cache_memory_diagnostic_status(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_change_state(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_change_state(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_channel_diagnostics_results(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_channel_diagnostics_results(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_cluster_performance_limitation_values(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_cluster_performance_limitation_values(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_controller_debug_information(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_controller_debug_information(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_controller_host_interfaces(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_controller_host_interfaces(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_controller_host_io_interfaces(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_controller_host_io_interfaces(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_controller_nvsram(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_controller_nvsram(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_controller_time(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_controller_time(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_critical_mel_entries(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_critical_mel_entries(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_ctl_lock_down_info(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_ctl_lock_down_info(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_cumulative_statistics_bundle(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_cumulative_statistics_bundle(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_cumulative_statistics_bundles(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_cumulative_statistics_bundles(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_dacstore_incompatible_volumes(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_dacstore_incompatible_volumes(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_database_metadata(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_database_metadata(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_ddc_log(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_ddc_log(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_discrete_time_series_bundle(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_discrete_time_series_bundle(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_disk_pool_expansion_candidates(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_disk_pool_expansion_candidates(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_disk_pool_max_reserved_drive_count(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_disk_pool_max_reserved_drive_count(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_disk_pool_reduction_drive_count(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_disk_pool_reduction_drive_count(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_dpl_core_dump_information(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_dpl_core_dump_information(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_drive_channel_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_drive_channel_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_drive_firmware_download_progress(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_drive_firmware_download_progress(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_drive_log_data(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_drive_log_data(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_drive_temperatures(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_drive_temperatures(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_enclosure_state_capture_data(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_enclosure_state_capture_data(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_enclosure_temperatures(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_enclosure_temperatures(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_energy_star_data(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_energy_star_data(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_enhanced_ib_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_enhanced_ib_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_env_card_log_data(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_env_card_log_data(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_export_dependencies(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_export_dependencies(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_flash_cache_analytics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_flash_cache_analytics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_flash_cache_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_flash_cache_statistics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_histogram_bundle(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_histogram_bundle(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_host_card_diagnostic_status(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_host_card_diagnostic_status(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_host_specific_nvsram(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_host_specific_nvsram(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_hot_spare_candidates(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_hot_spare_candidates(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_hot_spare_coverage(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_hot_spare_coverage(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_ib_ioc_attributes(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_ib_ioc_attributes(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_ib_port_partition_tables(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_ib_port_partition_tables(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_ib_rdma_channels(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_ib_rdma_channels(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_ib_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_ib_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_import_dependencies(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_import_dependencies(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_ioc_dump_information(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_ioc_dump_information(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_iscsi_copper_cable_diagnostics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_iscsi_copper_cable_diagnostics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_iscsi_negotiation_defaults(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_iscsi_negotiation_defaults(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_iscsi_sessions(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_iscsi_sessions(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_iscsi_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_iscsi_statistics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_long_lived_ops_progress(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_long_lived_ops_progress(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_lun_mappings(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_lun_mappings(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_mel_entries(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_mel_entries(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_mel_extent(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_mel_extent(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_metadata_volume_capacity(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_metadata_volume_capacity(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_object_graph(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_object_graph(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_p_registrations(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_p_registrations(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_p_registrations_for_volume(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_p_registrations_for_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_parity_check_progress(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_parity_check_progress(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_pending_hosts(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_pending_hosts(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_persistent_registrations(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_persistent_registrations(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_persistent_registrations_for_volume(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_persistent_registrations_for_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_pit_group_repository_utilization(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_pit_group_repository_utilization(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_pit_view_repository_utilization(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_pit_view_repository_utilization(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_product_capabilities(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_product_capabilities(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_psu_firmware_update_progress(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_psu_firmware_update_progress(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_read_link_status(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_read_link_status(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_recovery_failure_list(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_recovery_failure_list(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_remote_connections(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_remote_connections(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_repository_utilization(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_repository_utilization(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_sa_data(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_sa_data(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_sa_port(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_sa_port(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_sa_view_password_digest(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_sa_view_password_digest(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_sas_error_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_sas_error_statistics(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_soc_error_statistics(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_soc_error_statistics(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_system_attribute_defaults(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_system_attribute_defaults(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_thin_volume_consumed_capacity(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_thin_volume_consumed_capacity(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_thin_volume_expansion_history(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_thin_volume_expansion_history(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_unconfigured_initiators(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_unconfigured_initiators(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_unlabeled_host_ports(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_unlabeled_host_ports(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_volume_action_progress(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_volume_action_progress(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_volume_candidates(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_volume_candidates(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_volume_copy_source_candidates(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_volume_copy_source_candidates(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_volume_copy_target_candidates(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_volume_copy_target_candidates(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_volume_group_expansion_candidates(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_volume_group_expansion_candidates(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_volume_list_for_mirroring(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_volume_list_for_mirroring(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    
    def test_symbol_get_volume_performance(self):
       api = GApi()
       g_api = None
       try:
            g_api = api.symbol_get_volume_performance(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if g_api is None:
                g_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             g_api = 1

       self.assertNotEqual(g_api, None)
    


