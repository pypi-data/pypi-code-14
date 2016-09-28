#!/usr/bin/env python
# coding: utf-8

"""
e_api_test.py

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
from netapp.santricity.api.symbol.e_api import EApi



class EApiTest(unittest.TestCase):

    
    def test_symbol_enable_asup(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_enable_asup(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_enable_external_kms(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_enable_external_kms(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_enable_feature(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_enable_feature(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_enable_feature_evaluation(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_enable_feature_evaluation(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_enable_flash_cache_volume(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_enable_flash_cache_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_establish_volume_copy(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_establish_volume_copy(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_estimate_pit_rollback_repository_utilization(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_estimate_pit_rollback_repository_utilization(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_expand_concat_volume(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_expand_concat_volume(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_expand_thin_volume_virtual_capacity(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_expand_thin_volume_virtual_capacity(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_export_lock_key(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_export_lock_key(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_export_volume_group(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_export_volume_group(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    
    def test_symbol_external_kms_re_key(self):
       api = EApi()
       e_api = None
       try:
            e_api = api.symbol_external_kms_re_key(system_id="test", body="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if e_api is None:
                e_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             e_api = 1

       self.assertNotEqual(e_api, None)
    


