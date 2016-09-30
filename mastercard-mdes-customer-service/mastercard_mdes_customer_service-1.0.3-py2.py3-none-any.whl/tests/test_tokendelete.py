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
from mastercardmdescustomerservice import *


class TokenDeleteTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
                
    def test_example_mdes_token_delete(self):
        

        
    
        map = RequestMap()
        map.set("TokenDeleteRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        map.set("TokenDeleteRequest.CommentText", "Fraudulent transactions confirmed.")
        map.set("TokenDeleteRequest.ReasonCode", "T")
        map.set("TokenDeleteRequest.AuditInfo.UserId", "A1435477")
        map.set("TokenDeleteRequest.AuditInfo.UserName", "John Smith")
        map.set("TokenDeleteRequest.AuditInfo.Organization", "Any Bank")
        map.set("TokenDeleteRequest.AuditInfo.Phone", "5555551234")
        
        
        response = TokenDelete.create(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "TokenDeleteResponse.Token.TokenUniqueReference", response.get("TokenDeleteResponse.Token.TokenUniqueReference"),"DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        self.customAssertEqual(ignoreAsserts, "TokenDeleteResponse.Token.CommentId", response.get("TokenDeleteResponse.Token.CommentId"),"1234")
        

        BaseTest.putResponse("example_mdes_token_delete", response)
        

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

