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


class ConsumerContactID(BaseObject):
    """
    
    """

    __config = {
        "4227a86a-b6e8-460d-9e8c-fadf6e09adbd" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "query", [], []),
        "ffc31dc3-3af2-4928-8b14-8146ec2f5341" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "create", [], []),
        "0be53e24-4559-4e8d-9d49-074d7ebc840f" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "read", [], []),
        "dea282e2-ddeb-4423-8fa4-2ba99be16430" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "update", [], []),
        "1473b4a1-9e55-4b1f-a6e4-97bdfad93491" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "delete", [], []),
        
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
        Query objects of type ConsumerContactID by id and optional criteria
        @param type criteria
        @return ConsumerContactID object representing the response.
        """

        return BaseObject.execute("4227a86a-b6e8-460d-9e8c-fadf6e09adbd", ConsumerContactID(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ConsumerContactID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerContactID of the response of created instance.
        """
        return BaseObject.execute("ffc31dc3-3af2-4928-8b14-8146ec2f5341", ConsumerContactID(mapObj))











    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type ConsumerContactID by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerContactID
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("0be53e24-4559-4e8d-9d49-074d7ebc840f", ConsumerContactID(mapObj))



    def update(self):
        """
        Updates an object of type ConsumerContactID

        @return ConsumerContactID object representing the response.
        """
        return BaseObject.execute("dea282e2-ddeb-4423-8fa4-2ba99be16430", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerContactID by id

        @param str id
        @return ConsumerContactID of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("1473b4a1-9e55-4b1f-a6e4-97bdfad93491", ConsumerContactID(mapObj))


    def delete(self):
        """
        Delete object of type ConsumerContactID

        @return ConsumerContactID of the response of the deleted instance.
        """
        return BaseObject.execute("1473b4a1-9e55-4b1f-a6e4-97bdfad93491", self)




