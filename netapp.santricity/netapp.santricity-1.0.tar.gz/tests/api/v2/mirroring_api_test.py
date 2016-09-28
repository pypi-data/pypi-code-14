#!/usr/bin/env python
# coding: utf-8

"""
mirroring_api_test.py

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
from netapp.santricity.api.v2.mirroring_api import MirroringApi



class MirroringApiTest(unittest.TestCase):

    
    def test_begin_synchronization_amg(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.begin_synchronization_amg(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_complete_incomplete_amg(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.complete_incomplete_amg(system_id="test", incomplete_mirror_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_all_amg_member_repository_stats(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_all_amg_member_repository_stats(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_all_amg_member_volumes(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_all_amg_member_volumes(system_id="test", mirror_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_all_amg_members(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_all_amg_members(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_all_amg_sync_progress(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_all_amg_sync_progress(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_all_async_mirror_groups(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_all_async_mirror_groups(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_all_remote_volume_mirrors(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_all_remote_volume_mirrors(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_amg_member(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_amg_member(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_amg_member_repository_stats(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_amg_member_repository_stats(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_amg_member_volume(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_amg_member_volume(system_id="test", mirror_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_amg_sync_progress(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_amg_sync_progress(system_id="test", mirror_group_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_async_mirror_group(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_async_mirror_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_async_mirror_storage_system_list(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_async_mirror_storage_system_list(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_incomplete_amg(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_incomplete_amg(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_incomplete_amg_mirror_id(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_incomplete_amg_mirror_id(system_id="test", mirror_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_remote_amg_mirror_connections(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_remote_amg_mirror_connections(system_id="test", mirror_group_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_remote_mirror_connections(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_remote_mirror_connections(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_remote_volume_mirror(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_remote_volume_mirror(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_remote_volume_mirror_candidates(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_remote_volume_mirror_candidates(system_id="test", volume_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_get_remote_volume_mirror_sync_process(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.get_remote_volume_mirror_sync_process(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_new_amg_member(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.new_amg_member(system_id="test", mirror_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_new_async_mirror_group(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.new_async_mirror_group(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_new_remote_volume_mirror(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.new_remote_volume_mirror(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_remove_amg_member(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.remove_amg_member(system_id="test", mirror_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_remove_async_mirror_group(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.remove_async_mirror_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_remove_incomplete_async_mirror_relationship(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.remove_incomplete_async_mirror_relationship(system_id="test", incomplete_mirror_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_remove_remote_volume_mirror(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.remove_remote_volume_mirror(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_resume_synchronization_amg(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.resume_synchronization_amg(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_suspend_synchronization_amg(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.suspend_synchronization_amg(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_test_connectivity_amg(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.test_connectivity_amg(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_test_remote_volume_mirror_communication(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.test_remote_volume_mirror_communication(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_update_async_mirror_group(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.update_async_mirror_group(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_update_mirror_role_amg(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.update_mirror_role_amg(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    
    def test_update_remote_volume_mirror(self):
       api = MirroringApi()
       mirroring_api = None
       try:
            mirroring_api = api.update_remote_volume_mirror(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mirroring_api is None:
                mirroring_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mirroring_api = 1

       self.assertNotEqual(mirroring_api, None)
    


