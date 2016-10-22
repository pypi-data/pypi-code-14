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


class ApprovalTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
                
    def test_sample_create_approval(self):
        

        self.setAuthentication("vending_1")
    
        map = RequestMap()
        map.set("payload", "VGhpcyBpcyBkdW1teSBwYXlsb2Fk")
        
        
        response = Approval.create(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "amount", response.get("amount"),"100")
        self.customAssertEqual(ignoreAsserts, "approvalPayload", response.get("approvalPayload"),"VGhpcyBpcyBkdW1teSBwYXlsb2Fk")
        self.customAssertEqual(ignoreAsserts, "id", response.get("id"),"t18dijsg7tll0276prfhmh7e3m")
        self.customAssertEqual(ignoreAsserts, "previous.id", response.get("previous.id"),"fdf87660-5f9a-11e6-9ac9-f90191c8e88a")
        self.customAssertEqual(ignoreAsserts, "previous.state", response.get("previous.state"),"vendsuccess")
        self.customAssertEqual(ignoreAsserts, "sessionId", response.get("sessionId"),"e879c950-6eaa-11e6-bc0a-dd0448c2e796")
        

        BaseTest.putResponse("sample_create_approval", response)
        self.resetAuthentication()

    
        
        
        
        
        
        
    
        
        
                
    def test_sample_update_approval(self):
        

        self.setAuthentication("vending_1")
    
        map = RequestMap()
        map.set("id", "t18dijsg7tll0276prfhmh7e3m")
        map.set("payload", "VGhpcyBpcyBkdW1teSBwYXlsb2Fk")
        
        
        response = Approval(map).update()

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "amount", response.get("amount"),"500")
        self.customAssertEqual(ignoreAsserts, "id", response.get("id"),"t18dijsg7tll0276prfhmh7e3m")
        self.customAssertEqual(ignoreAsserts, "sessionId", response.get("sessionId"),"e879c950-6eaa-11e6-bc0a-dd0448c2e796")
        self.customAssertEqual(ignoreAsserts, "state", response.get("state"),"vendsuccess")
        

        BaseTest.putResponse("sample_update_approval", response)
        self.resetAuthentication()

    
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

