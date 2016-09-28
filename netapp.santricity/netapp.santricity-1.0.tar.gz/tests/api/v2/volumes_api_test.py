#!/usr/bin/env python
# coding: utf-8

"""
volumes_api_test.py

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
from netapp.santricity.api.v2.volumes_api import VolumesApi



class VolumesApiTest(unittest.TestCase):

    
    def test_change_raid_type(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.change_raid_type(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_expand_storage_pool_capacity(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.expand_storage_pool_capacity(system_id="test", pool_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_expand_thin_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.expand_thin_volume(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_expand_thin_volume_capacity_old(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.expand_thin_volume_capacity_old(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_export_fde_key(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.export_fde_key(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_access_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_access_volume(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_all_lun_mappings(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_all_lun_mappings(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_all_mappable_objects(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_all_mappable_objects(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_all_storage_pools(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_all_storage_pools(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_all_thin_volumes(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_all_thin_volumes(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_all_volumes(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_all_volumes(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_lun_mapping(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_lun_mapping(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_mappable_object(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_mappable_object(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_storage_pool(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_storage_pool(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_storage_pool_expansion_candidates(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_storage_pool_expansion_candidates(system_id="test", pool_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_storage_pool_progress(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_storage_pool_progress(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_storage_pool_removable_drives(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_storage_pool_removable_drives(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_thin_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_thin_volume(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_thin_volume2(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_thin_volume2(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_thin_volumes2(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_thin_volumes2(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_volume(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_volume_expansion_progress(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_volume_expansion_progress(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_get_volume_expansion_progress2(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.get_volume_expansion_progress2(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_import_fde_key(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.import_fde_key(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_initialize_thin_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.initialize_thin_volume(system_id="test", thin_volume_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_initialize_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.initialize_volume(system_id="test", volume_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_move_lun_mapping(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.move_lun_mapping(system_id="test", mapping_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_new_fde_key(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.new_fde_key(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_new_lun_mapping(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.new_lun_mapping(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_new_storage_pool(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.new_storage_pool(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_new_thin_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.new_thin_volume(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_new_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.new_volume(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_remove_lun_mapping(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.remove_lun_mapping(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_remove_storage_pool(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.remove_storage_pool(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_remove_storage_pool_drive(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.remove_storage_pool_drive(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_remove_thin_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.remove_thin_volume(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_remove_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.remove_volume(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_start_volume_expansion(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.start_volume_expansion(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_start_volume_expansion2(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.start_volume_expansion2(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_update_storage_pool(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.update_storage_pool(system_id="test", id="test", request="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_update_thin_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.update_thin_volume(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_update_volume(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.update_volume(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    
    def test_validate_fde_key(self):
       api = VolumesApi()
       volumes_api = None
       try:
            volumes_api = api.validate_fde_key(system_id="test", keyfile="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if volumes_api is None:
                volumes_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             volumes_api = 1

       self.assertNotEqual(volumes_api, None)
    


