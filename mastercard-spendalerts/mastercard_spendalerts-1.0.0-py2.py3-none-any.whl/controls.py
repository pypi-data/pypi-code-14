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
from sdkconfig import SDKConfig


class Controls(BaseObject):
    """
    
    """

    __config = {
        "90b39987-b580-43ad-9ca6-9e20e67fad3a" : OperationConfig("/issuer/v1/card/{uuid}/controls", "query", [], []),
        "e19e4579-c8d6-4e38-9abd-3d2eb52ab463" : OperationConfig("/issuer/v1/card/{uuid}/controls", "create", [], []),
        "1ddb49ea-ea7a-4403-9c32-30680ab55e06" : OperationConfig("/issuer/v1/card/{uuid}/controls", "delete", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUI)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(SDKConfig.getVersion(), SDKConfig.getHost())






    @classmethod
    def query(cls,criteria):
        """
        Query objects of type Controls by id and optional criteria
        @param type criteria
        @return Controls object representing the response.
        """

        return BaseObject.execute("90b39987-b580-43ad-9ca6-9e20e67fad3a", Controls(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Controls

        @param Dict mapObj, containing the required parameters to create a new object
        @return Controls of the response of created instance.
        """
        return BaseObject.execute("e19e4579-c8d6-4e38-9abd-3d2eb52ab463", Controls(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Controls by id

        @param str id
        @return Controls of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("1ddb49ea-ea7a-4403-9c32-30680ab55e06", Controls(mapObj))


    def delete(self):
        """
        Delete object of type Controls

        @return Controls of the response of the deleted instance.
        """
        return BaseObject.execute("1ddb49ea-ea7a-4403-9c32-30680ab55e06", self)




