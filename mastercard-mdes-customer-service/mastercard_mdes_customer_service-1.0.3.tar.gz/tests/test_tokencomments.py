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


class TokenCommentsTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
                
    def test_example_mdes_token_comments(self):
        

        
    
        map = RequestMap()
        map.set("TokenCommentsRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        map.set("TokenCommentsRequest.AuditInfo.UserId", "A1435477")
        map.set("TokenCommentsRequest.AuditInfo.UserName", "John Smith")
        map.set("TokenCommentsRequest.AuditInfo.Organization", "Any Bank")
        map.set("TokenCommentsRequest.AuditInfo.Phone", "5555551234")
        
        
        response = TokenComments.create(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[0].CommentId", response.get("TokenCommentsResponse.Comments.Comment[0].CommentId"),"1648")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[0].CommentText", response.get("TokenCommentsResponse.Comments.Comment[0].CommentText"),"Cardholder lost phone. Suspending device.")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[0].CommentDateTime", response.get("TokenCommentsResponse.Comments.Comment[0].CommentDateTime"),"2015-01-21T18:04:35-06:00")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[0].AuditInfo.UserId", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.UserId"),"A14354774")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[0].AuditInfo.UserName", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.UserName"),"Jade Mark")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[0].AuditInfo.Organization", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.Organization"),"Any Bank")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[0].AuditInfo.Phone", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.Phone"),"5555558888")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[1].CommentId", response.get("TokenCommentsResponse.Comments.Comment[1].CommentId"),"1647")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[1].CommentText", response.get("TokenCommentsResponse.Comments.Comment[1].CommentText"),"Cardholder called to activate their digital card.")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[1].CommentDateTime", response.get("TokenCommentsResponse.Comments.Comment[1].CommentDateTime"),"2015-01-19T11:02:25-06:00")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[1].AuditInfo.UserId", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.UserId"),"A14354773")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[1].AuditInfo.UserName", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.UserName"),"Tom Smith")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[1].AuditInfo.Organization", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.Organization"),"Any Bank")
        self.customAssertEqual(ignoreAsserts, "TokenCommentsResponse.Comments.Comment[1].AuditInfo.Phone", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.Phone"),"5555559999")
        

        BaseTest.putResponse("example_mdes_token_comments", response)
        

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

