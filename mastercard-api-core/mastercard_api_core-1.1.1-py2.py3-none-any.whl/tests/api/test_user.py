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
from user import User

class UserTest2(BaseTest):

    def setUp(self):
        keyFile = join(dirname(dirname(realpath(__file__))),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d", keyFile, "alias", "password")
        Config.setAuthentication(auth)
    
        
        
        
                
    def test_list_users(self):
        mapObj = RequestMap()
        

        

        ignoreAsserts = []
        

        response = User.listByCriteria(mapObj)
        self.customAssertEqual(ignoreAsserts, "website", response.get("list[0].website"),"hildegard.org")
        self.customAssertEqual(ignoreAsserts, "address.instructions.doorman", response.get("list[0].address.instructions.doorman"),"true")
        self.customAssertEqual(ignoreAsserts, "address.instructions.text", response.get("list[0].address.instructions.text"),"some delivery instructions text")
        self.customAssertEqual(ignoreAsserts, "address.city", response.get("list[0].address.city"),"New York")
        self.customAssertEqual(ignoreAsserts, "address.postalCode", response.get("list[0].address.postalCode"),"10577")
        self.customAssertEqual(ignoreAsserts, "address.id", response.get("list[0].address.id"),"1")
        self.customAssertEqual(ignoreAsserts, "address.state", response.get("list[0].address.state"),"NY")
        self.customAssertEqual(ignoreAsserts, "address.line1", response.get("list[0].address.line1"),"2000 Purchase Street")
        self.customAssertEqual(ignoreAsserts, "phone", response.get("list[0].phone"),"1-770-736-8031")
        self.customAssertEqual(ignoreAsserts, "name", response.get("list[0].name"),"Joe Bloggs")
        self.customAssertEqual(ignoreAsserts, "id", response.get("list[0].id"),"1")
        self.customAssertEqual(ignoreAsserts, "email", response.get("list[0].email"),"name@example.com")
        self.customAssertEqual(ignoreAsserts, "username", response.get("list[0].username"),"jbloggs")
        

        BaseTest.putResponse("list_users", response.get("list[0]"));

    
    def test_list_users_query(self):
        mapObj = RequestMap()
        mapObj.set("max", "10")
        

        

        ignoreAsserts = []
        

        response = User.listByCriteria(mapObj)
        self.customAssertEqual(ignoreAsserts, "website", response.get("list[0].website"),"hildegard.org")
        self.customAssertEqual(ignoreAsserts, "address.instructions.doorman", response.get("list[0].address.instructions.doorman"),"true")
        self.customAssertEqual(ignoreAsserts, "address.instructions.text", response.get("list[0].address.instructions.text"),"some delivery instructions text")
        self.customAssertEqual(ignoreAsserts, "address.city", response.get("list[0].address.city"),"New York")
        self.customAssertEqual(ignoreAsserts, "address.postalCode", response.get("list[0].address.postalCode"),"10577")
        self.customAssertEqual(ignoreAsserts, "address.id", response.get("list[0].address.id"),"1")
        self.customAssertEqual(ignoreAsserts, "address.state", response.get("list[0].address.state"),"NY")
        self.customAssertEqual(ignoreAsserts, "address.line1", response.get("list[0].address.line1"),"2000 Purchase Street")
        self.customAssertEqual(ignoreAsserts, "phone", response.get("list[0].phone"),"1-770-736-8031")
        self.customAssertEqual(ignoreAsserts, "name", response.get("list[0].name"),"Joe Bloggs")
        self.customAssertEqual(ignoreAsserts, "id", response.get("list[0].id"),"1")
        self.customAssertEqual(ignoreAsserts, "email", response.get("list[0].email"),"name@example.com")
        self.customAssertEqual(ignoreAsserts, "username", response.get("list[0].username"),"jbloggs")
        

        BaseTest.putResponse("list_users_query", response.get("list[0]"));

    
        
        
        
        
    
        
                
    def test_create_user(self):
        mapObj = RequestMap()
        mapObj.set("website", "hildegard.org")
        mapObj.set("address.city", "New York")
        mapObj.set("address.postalCode", "10577")
        mapObj.set("address.state", "NY")
        mapObj.set("address.line1", "2000 Purchase Street")
        mapObj.set("phone", "1-770-736-8031")
        mapObj.set("name", "Joe Bloggs")
        mapObj.set("email", "name@example.com")
        mapObj.set("username", "jbloggs")
        

        

        ignoreAsserts = []
        

        response = User.create(mapObj)

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
        

        BaseTest.putResponse("create_user", response);

    
        
        
        
        
        
        
    
        
        
        
        
        
                
    def test_get_user(self):
        id = ""
        map = RequestMap()
        

        map.set("id", BaseTest.resolveResponseValue("create_user.id"));
        

        ignoreAsserts = []
        ignoreAsserts.append("address.city");
        

        response = User.read(id,map)
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
        

        BaseTest.putResponse("get_user", response);

    
    def test_get_user_query(self):
        id = ""
        map = RequestMap()
        map.set("min", "1")
        map.set("max", "10")
        

        map.set("id", BaseTest.resolveResponseValue("create_user.id"));
        

        ignoreAsserts = []
        

        response = User.read(id,map)
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
        

        BaseTest.putResponse("get_user_query", response);

    
        
        
    
        
        
                
    def test_update_user(self):
        mapObj = RequestMap()
        mapObj.set("name", "Joe Bloggs")
        mapObj.set("username", "jbloggs")
        mapObj.set("email", "name@example.com")
        mapObj.set("phone", "1-770-736-8031")
        mapObj.set("website", "hildegard.org")
        mapObj.set("address.line1", "2000 Purchase Street")
        mapObj.set("address.city", "New York")
        mapObj.set("address.state", "NY")
        mapObj.set("address.postalCode", "10577")
        

        mapObj.set("id", BaseTest.resolveResponseValue("create_user.id"));
        

        ignoreAsserts = []
        

        request = User(mapObj)
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
        

        BaseTest.putResponse("update_user", response);

    
        
        
        
        
        
    
        
        
        
        
                
    def test_delete_user(self):
        map = RequestMap()
        

        map.set("id", BaseTest.resolveResponseValue("create_user.id"));
        

        ignoreAsserts = []
        

        response = User.deleteById("ssss",map)
        self.assertNotEqual(response,None)
        

        BaseTest.putResponse("delete_user", response);

    

        
        
        
    

if __name__ == '__main__':
    unittest.main()

