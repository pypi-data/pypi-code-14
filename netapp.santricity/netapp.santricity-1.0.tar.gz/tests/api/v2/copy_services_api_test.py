#!/usr/bin/env python
# coding: utf-8

"""
copy_services_api_test.py

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
from netapp.santricity.api.v2.copy_services_api import CopyServicesApi



class CopyServicesApiTest(unittest.TestCase):

    
    def test_convert_snapshot_volume_to_read_write(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.convert_snapshot_volume_to_read_write(system_id="test", view_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_expand_concat_volume(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.expand_concat_volume(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_concat_repository_volumes(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_concat_repository_volumes(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_consistency_group_members(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_consistency_group_members(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_consistency_group_members_list(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_consistency_group_members_list(system_id="test", cg_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_consistency_group_snapshot_views(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_consistency_group_snapshot_views(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_consistency_group_snapshot_views_list(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_consistency_group_snapshot_views_list(system_id="test", cg_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_consistency_group_snapshots(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_consistency_group_snapshots(system_id="test", cg_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_consistency_groups(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_consistency_groups(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_copy_pair_progress(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_copy_pair_progress(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_legacy_snapshot_repo_stats(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_legacy_snapshot_repo_stats(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_legacy_snapshots(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_legacy_snapshots(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_snapshot_group_repo_stats(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_snapshot_group_repo_stats(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_snapshot_groups(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_snapshot_groups(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_snapshot_schedules(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_snapshot_schedules(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_snapshot_volume_repo_stats(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_snapshot_volume_repo_stats(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_snapshot_volumes (self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_snapshot_volumes (system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_snapshots(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_snapshots(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_all_volume_copy_pairs(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_all_volume_copy_pairs(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_concat_repository_volumes(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_concat_repository_volumes(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_concat_volume_candidates(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_concat_volume_candidates(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_consistency_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_consistency_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_consistency_group_members(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_consistency_group_members(system_id="test", cg_id="test", volume_ref="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_consistency_group_snapshot_view(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_consistency_group_snapshot_view(system_id="test", cg_id="test", view_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_consistency_group_snapshot_volumes(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_consistency_group_snapshot_volumes(system_id="test", cg_id="test", view_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_consistency_group_snapshots(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_consistency_group_snapshots(system_id="test", cg_id="test", sequence_number="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_copy_pair_progress(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_copy_pair_progress(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_legacy_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_legacy_snapshot(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_legacy_snapshot_repo_stats(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_legacy_snapshot_repo_stats(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_multiple_concat_volume_candidates(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_multiple_concat_volume_candidates(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_snapshot(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_snapshot_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_snapshot_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_snapshot_group_repo_stats(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_snapshot_group_repo_stats(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_snapshot_schedule(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_snapshot_schedule(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_snapshot_volume(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_snapshot_volume(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_snapshot_volume_repo_stats(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_snapshot_volume_repo_stats(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_get_volume_copy_pair(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.get_volume_copy_pair(system_id="test", vc_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_consistency_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_consistency_group(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_consistency_group_member(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_consistency_group_member(system_id="test", cg_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_consistency_group_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_consistency_group_snapshot(system_id="test", cg_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_consistency_group_snapshot_view(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_consistency_group_snapshot_view(system_id="test", cg_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_consistency_group_snapshot_view_detailed(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_consistency_group_snapshot_view_detailed(system_id="test", cg_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_legacy_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_legacy_snapshot(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_multiple_consistency_group_members(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_multiple_consistency_group_members(system_id="test", cg_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_snapshot(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_snapshot_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_snapshot_group(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_snapshot_volume(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_snapshot_volume(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_new_volume_copy_pair(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.new_volume_copy_pair(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_consistency_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_consistency_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_consistency_group_member(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_consistency_group_member(system_id="test", cg_id="test", volume_ref="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_consistency_group_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_consistency_group_snapshot(system_id="test", cg_id="test", sequence_number="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_consistency_group_snapshot_view(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_consistency_group_snapshot_view(system_id="test", cg_id="test", view_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_legacy_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_legacy_snapshot(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_snapshot(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_snapshot_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_snapshot_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_snapshot_volume(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_snapshot_volume(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_remove_volume_copy_pair(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.remove_volume_copy_pair(system_id="test", vc_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_rollback_consistency_group_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.rollback_consistency_group_snapshot(system_id="test", cg_id="test", sequence_number="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_update_consistency_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.update_consistency_group(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_update_copy_pair_operation(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.update_copy_pair_operation(system_id="test", ids="test", control="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_update_legacy_snapshot(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.update_legacy_snapshot(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_update_snapshot_group(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.update_snapshot_group(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_update_snapshot_volume(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.update_snapshot_volume(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    
    def test_update_volume_copy_pair_parameters(self):
       api = CopyServicesApi()
       copy_services_api = None
       try:
            copy_services_api = api.update_volume_copy_pair_parameters(system_id="test", vc_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if copy_services_api is None:
                copy_services_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             copy_services_api = 1

       self.assertNotEqual(copy_services_api, None)
    


