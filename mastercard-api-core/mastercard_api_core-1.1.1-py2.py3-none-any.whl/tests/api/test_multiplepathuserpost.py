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
from mastercardapicore import RequestMap, Config, OAuthAuthentication
from os.path import dirname, realpath, join
from base_test import BaseTest
from multiplepathuserpost import MultiplePathUserPost


class MultiplePathUserPostTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(dirname(realpath(__file__))),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d", keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
                
    def test_get_user_posts_with_mutplie_path(self):
        mapObj = RequestMap()
        mapObj.set("user_id", "1")
        mapObj.set("post_id", "2")
        

        

        ignoreAsserts = []
        

        response = MultiplePathUserPost.listByCriteria(mapObj)
        self.customAssertEqual(ignoreAsserts, "id", response.get("list[0].id"),"1")
        self.customAssertEqual(ignoreAsserts, "title", response.get("list[0].title"),"My Title")
        self.customAssertEqual(ignoreAsserts, "body", response.get("list[0].body"),"some body text")
        self.customAssertEqual(ignoreAsserts, "userId", response.get("list[0].userId"),"1")
        

        BaseTest.putResponse("get_user_posts_with_mutplie_path", response.get("list[0]"));

    
        
        
        
        
    
        
        
                
    def test_update_user_posts_with_mutplie_path(self):
        mapObj = RequestMap()
        mapObj.set("user_id", "1")
        mapObj.set("post_id", "1")
        mapObj.set("testQuery", "testQuery")
        mapObj.set("name", "Joe Bloggs")
        mapObj.set("username", "jbloggs")
        mapObj.set("email", "name@example.com")
        mapObj.set("phone", "1-770-736-8031")
        mapObj.set("website", "hildegard.org")
        mapObj.set("address.line1", "2000 Purchase Street")
        mapObj.set("address.city", "New York")
        mapObj.set("address.state", "NY")
        mapObj.set("address.postalCode", "10577")
        

        

        ignoreAsserts = []
        

        request = MultiplePathUserPost(mapObj)
        response = request.update()
        self.customAssertEqual(ignoreAsserts, "website", response.get("website"),"hildegard.org")
        self.customAssertEqual(ignoreAsserts, "address.instructions.doorman", response.get("address.instructions.doorman"),"true")
        self.customAssertEqual(ignoreAsserts, "address.instructions.text", response.get("address.instructions.text"),"some delivery instructions text")
        self.customAssertEqual(ignoreAsserts, "address.city", response.get("address.city"),"New York")
        self.customAssertEqual(ignoreAsserts, "address.postalCode", response.get("address.postalCode"),"10577")
        self.customAssertEqual(ignoreAsserts, "address.id", response.get("address.id"),"1")
        self.customAssertEqual(ignoreAsserts, "address.state", response.get("address.state"),"NY")
        self.customAssertEqual(ignoreAsserts, "address.line1", response.get("address.line1"),"2000 Purchase Street")
        self.customAssertEqual(ignoreAsserts, "phone", response.get("phone"),"1-770-736-8031")
        self.customAssertEqual(ignoreAsserts, "name", response.get("name"),"Joe Bloggs")
        self.customAssertEqual(ignoreAsserts, "id", response.get("id"),"1")
        self.customAssertEqual(ignoreAsserts, "email", response.get("email"),"name@example.com")
        self.customAssertEqual(ignoreAsserts, "username", response.get("username"),"jbloggs")
        

        BaseTest.putResponse("update_user_posts_with_mutplie_path", response);

    
        
        
        
        
        
    
        
        
        
        
                
    def test_delete_user_posts_with_mutplie_path(self):
        map = RequestMap()
        map.set("user_id", "1")
        map.set("post_id", "2")
        

        

        ignoreAsserts = []
        

        response = MultiplePathUserPost.deleteById("",map)
        self.assertNotEqual(response,None)
        

        BaseTest.putResponse("delete_user_posts_with_mutplie_path", response);

    

        
        
        
    

if __name__ == '__main__':
    unittest.main()

