#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

import unittest
import time
from mastercardapicore import RequestMap
from base_test import BaseTest
from mastercardvending import *


class MachineTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
                
    def test_sample_machines_nearby(self):
        

        self.setAuthentication("vending_1")
    
        map = RequestMap()
        map.set("latitude", "36.121174")
        map.set("longitude", "-115.169609")
        
        
        response = Machine.listByCriteria(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "address", response.get("list[0].address"),"3355 S Las Vegas Blvd The Venetian")
        self.customAssertEqual(ignoreAsserts, "description", response.get("list[0].description"),"Soft drinks and snacks available for sale")
        self.customAssertEqual(ignoreAsserts, "distance", response.get("list[0].distance"),"0.0")
        self.customAssertEqual(ignoreAsserts, "latitude", response.get("list[0].latitude"),"36.121174")
        self.customAssertEqual(ignoreAsserts, "longitude", response.get("list[0].longitude"),"-115.16961")
        self.customAssertEqual(ignoreAsserts, "model", response.get("list[0].model"),"1")
        self.customAssertEqual(ignoreAsserts, "name", response.get("list[0].name"),"Mastercard Vending 1")
        self.customAssertEqual(ignoreAsserts, "serial", response.get("list[0].serial"),"1017")
        self.customAssertEqual(ignoreAsserts, "serviceId", response.get("list[0].serviceId"),"fff0")
        

        BaseTest.putResponse("sample_machines_nearby", response.get("list[0]"))
        self.resetAuthentication()

    
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

