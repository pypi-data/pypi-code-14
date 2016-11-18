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


class ConsumerGovernmentID(BaseObject):
    """
    
    """

    __config = {
        "294368a4-d216-446c-bcb7-4347899ed8a0" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "query", [], []),
        "e9feb4e2-c273-4a66-a302-d817dfe77410" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "create", [], []),
        "589c6f34-a3c6-4b53-9305-68989e84ef25" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "read", [], []),
        "d27aa73e-5107-4219-9ae1-367a9da4c937" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "update", [], []),
        "85466f69-1d63-491a-ae9a-902e5566937d" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "delete", [], []),
        
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
        Query objects of type ConsumerGovernmentID by id and optional criteria
        @param type criteria
        @return ConsumerGovernmentID object representing the response.
        """

        return BaseObject.execute("294368a4-d216-446c-bcb7-4347899ed8a0", ConsumerGovernmentID(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ConsumerGovernmentID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerGovernmentID of the response of created instance.
        """
        return BaseObject.execute("e9feb4e2-c273-4a66-a302-d817dfe77410", ConsumerGovernmentID(mapObj))











    @classmethod
    def read(cls,id,criteria=None):
        """
        Returns objects of type ConsumerGovernmentID by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of ConsumerGovernmentID
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("589c6f34-a3c6-4b53-9305-68989e84ef25", ConsumerGovernmentID(mapObj))



    def update(self):
        """
        Updates an object of type ConsumerGovernmentID

        @return ConsumerGovernmentID object representing the response.
        """
        return BaseObject.execute("d27aa73e-5107-4219-9ae1-367a9da4c937", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type ConsumerGovernmentID by id

        @param str id
        @return ConsumerGovernmentID of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("85466f69-1d63-491a-ae9a-902e5566937d", ConsumerGovernmentID(mapObj))


    def delete(self):
        """
        Delete object of type ConsumerGovernmentID

        @return ConsumerGovernmentID of the response of the deleted instance.
        """
        return BaseObject.execute("85466f69-1d63-491a-ae9a-902e5566937d", self)




