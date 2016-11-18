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


class ConsumerAccount(BaseObject):
    """
    
    """

    __config = {
        "8485ebeb-4461-466a-8e3f-013f591efe8e" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts", "query", [], ["ref"]),
        "acfc4989-7ef9-4142-948d-5b6879605a62" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts", "create", [], []),
        "101cf482-bc21-418e-9297-a489960fd46f" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts/{accountId}", "read", [], []),
        "d753e12c-70c2-49b5-85d0-d2bf1d5737db" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts/{accountId}", "update", [], []),
        "4bbc4b2a-943f-4373-b231-96b97c971979" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/accounts/{accountId}", "delete", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUI)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(SDKConfig.getVersion(), SDKConfig.getHost())






    @classmethod
    def listAll(cls,criteria):
        """
        Query objects of type ConsumerAccount by id and optional criteria
        @param type criteria
        @return ConsumerAccount object representing the response.
        """

        return BaseObject.execute("8485ebeb-4461-466a-8e3f-013f591efe8e", ConsumerAccount(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ConsumerAccount

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerAccount of the response of created instance.
        """
        return BaseObject.execute("acfc4989-7ef9-4142-948d-5b6879605a62", ConsumerAccount(mapObj))











    @classmethod
    def readByID(cls,id,criteria=None):
        """
        Returns objects of type ConsumerAccount by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerAccount
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("101cf482-bc21-418e-9297-a489960fd46f", ConsumerAccount(mapObj))



    def update(self):
        """
        Updates an object of type ConsumerAccount

        @return ConsumerAccount object representing the response.
        """
        return BaseObject.execute("d753e12c-70c2-49b5-85d0-d2bf1d5737db", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerAccount by id

        @param str id
        @return ConsumerAccount of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("4bbc4b2a-943f-4373-b231-96b97c971979", ConsumerAccount(mapObj))


    def delete(self):
        """
        Delete object of type ConsumerAccount

        @return ConsumerAccount of the response of the deleted instance.
        """
        return BaseObject.execute("4bbc4b2a-943f-4373-b231-96b97c971979", self)




