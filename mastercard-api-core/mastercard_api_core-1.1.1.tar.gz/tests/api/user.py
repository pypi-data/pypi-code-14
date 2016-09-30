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


from mastercardapicore.core.model import BaseObject
from mastercardapicore.core.model import RequestMap
from mastercardapicore.core.model import OperationConfig
from mastercardapicore.core.model import OperationMetadata


class User(BaseObject):
    """
    
    """

    __config = {
        "9ded5f43-1db6-428a-aef5-c8f849f190a8" : OperationConfig("/mock_crud_server/users", "list", [], []),
        "7187d685-71a8-4d2e-8a95-72ef94cac718" : OperationConfig("/mock_crud_server/users", "create", [], []),
        "a0aec5ec-9deb-4b1f-a5a4-f8d6db59645d" : OperationConfig("/mock_crud_server/users/{id}", "read", [], []),
        "16a66c62-624e-42ef-9d1b-3634a23963d2" : OperationConfig("/mock_crud_server/users/{id}", "update", [], []),
        "37bd1253-3d58-48b2-b6a4-6e4d2bec81a4" : OperationConfig("/mock_crud_server/users/{id}", "delete", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUI)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata("0.0.1", "http://localhost:8081")



    @classmethod
    def listByCriteria(cls,criteria=None):
        """
        List objects of type User

        @param Dict criteria
        @return Array of User object matching the criteria.
        """

        if criteria is None:
            return BaseObject.execute("9ded5f43-1db6-428a-aef5-c8f849f190a8", User())
        else:
            return BaseObject.execute("9ded5f43-1db6-428a-aef5-c8f849f190a8", User(criteria))



    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type User

        @param Dict mapObj, containing the required parameters to create a new object
        @return User of the response of created instance.
        """
        return BaseObject.execute("7187d685-71a8-4d2e-8a95-72ef94cac718", User(mapObj))











    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type User by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of User
        """
        mapObj =  RequestMap()
        if id != None:
            mapObj.set("id", id)

        if criteria != None:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("a0aec5ec-9deb-4b1f-a5a4-f8d6db59645d", User(mapObj))



    def update(self):
        """
        Updates an object of type User

        @return User object representing the response.
        """
        return BaseObject.execute("16a66c62-624e-42ef-9d1b-3634a23963d2", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type User by id

        @param str id
        @return User of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id != None:
            mapObj.set("id", id)

        if map != None:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("37bd1253-3d58-48b2-b6a4-6e4d2bec81a4", User(mapObj))


    def delete(self):
        """
        Delete object of type User

        @return User of the response of the deleted instance.
        """
        return BaseObject.execute("37bd1253-3d58-48b2-b6a4-6e4d2bec81a4", self)




