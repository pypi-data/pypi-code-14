#!/usr/bin/env python
# coding: utf-8

"""
mapping_api_test.py

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
from netapp.santricity.api.v2.mapping_api import MappingApi



class MappingApiTest(unittest.TestCase):

    
    def test_get_all_host_groups(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_all_host_groups(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_all_host_port_types(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_all_host_port_types(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_all_host_type_values(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_all_host_type_values(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_all_host_types(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_all_host_types(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_all_hosts(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_all_hosts(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_host(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_host(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_host_group(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_host_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_host_port_type(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_host_port_type(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_host_type(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_host_type(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_host_type_values(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_host_type_values(system_id="test", index="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_get_unassociated_host_ports(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.get_unassociated_host_ports(system_id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_move_host(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.move_host(system_id="test", host_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_new_host(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.new_host(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_new_host_group(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.new_host_group(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_remove_host(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.remove_host(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_remove_host_group(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.remove_host_group(system_id="test", id="test")
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_set_host_port_type_default(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.set_host_port_type_default(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_set_host_type_default(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.set_host_type_default(system_id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_update_host(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.update_host(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    
    def test_update_host_group(self):
       api = MappingApi()
       mapping_api = None
       try:
            mapping_api = api.update_host_group(system_id="test", id="test", )
            # For the DELETE calls, there's no reponse returned and we want to set that as a valid sdk call.
            if mapping_api is None:
                mapping_api = 1
       except (ApiException, IOError)  as exp:
             # The API call went through but got a HTTP errorcode, which means the SDK works
             mapping_api = 1

       self.assertNotEqual(mapping_api, None)
    


