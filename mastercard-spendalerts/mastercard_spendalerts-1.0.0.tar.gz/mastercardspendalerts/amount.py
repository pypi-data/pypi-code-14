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


class Amount(BaseObject):
    """
    
    """

    __config = {
        "feeb4cba-7afb-46cc-9ba2-6e03a5a9fe0b" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/transactionamount", "query", [], []),
        "b2e24b11-c85f-4339-94ab-43559965a2ac" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/transactionamount", "create", [], []),
        "3183a937-5e52-48b5-8fad-2a374ae7d9c8" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/transactionamount", "delete", [], []),
        
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
        Query objects of type Amount by id and optional criteria
        @param type criteria
        @return Amount object representing the response.
        """

        return BaseObject.execute("feeb4cba-7afb-46cc-9ba2-6e03a5a9fe0b", Amount(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Amount

        @param Dict mapObj, containing the required parameters to create a new object
        @return Amount of the response of created instance.
        """
        return BaseObject.execute("b2e24b11-c85f-4339-94ab-43559965a2ac", Amount(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Amount by id

        @param str id
        @return Amount of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("3183a937-5e52-48b5-8fad-2a374ae7d9c8", Amount(mapObj))


    def delete(self):
        """
        Delete object of type Amount

        @return Amount of the response of the deleted instance.
        """
        return BaseObject.execute("3183a937-5e52-48b5-8fad-2a374ae7d9c8", self)




