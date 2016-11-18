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


class Consumer(BaseObject):
    """
    
    """

    __config = {
        "c1b5955e-fdbd-434d-9ced-9923693b5e9b" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "query", [], ["ref","contact_id_uri"]),
        "7801aee1-b1a1-4a0d-9a09-3c3b4f8cb71b" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "create", [], []),
        "7373c2cd-c275-41be-bde8-4c104f8d5cc0" : OperationConfig("/send/v1/partners/{partnerId}/consumers/search", "create", [], []),
        "c5b3c0b3-6fda-4bbf-87b8-33f1901ad66a" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "read", [], []),
        "ebb0f3b5-4cbe-4184-949d-c414050180e3" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "update", [], []),
        "7dde0a74-bf80-4bd8-aa64-9603f9b368af" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "delete", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUI)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(SDKConfig.getVersion(), SDKConfig.getHost())






    @classmethod
    def listByReferenceOrContactID(cls,criteria):
        """
        Query objects of type Consumer by id and optional criteria
        @param type criteria
        @return Consumer object representing the response.
        """

        return BaseObject.execute("c1b5955e-fdbd-434d-9ced-9923693b5e9b", Consumer(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        """
        return BaseObject.execute("7801aee1-b1a1-4a0d-9a09-3c3b4f8cb71b", Consumer(mapObj))






    @classmethod
    def listByReferenceContactIDOrGovernmentID(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        """
        return BaseObject.execute("7373c2cd-c275-41be-bde8-4c104f8d5cc0", Consumer(mapObj))











    @classmethod
    def readByID(cls,id,criteria=None):
        """
        Returns objects of type Consumer by id and optional criteria
        @param str id
        @param dict criteria
        @return instance of Consumer
        """
        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if criteria:
            if (isinstance(criteria,RequestMap)):
                mapObj.setAll(criteria.getObject())
            else:
                mapObj.setAll(criteria)

        return BaseObject.execute("c5b3c0b3-6fda-4bbf-87b8-33f1901ad66a", Consumer(mapObj))



    def update(self):
        """
        Updates an object of type Consumer

        @return Consumer object representing the response.
        """
        return BaseObject.execute("ebb0f3b5-4cbe-4184-949d-c414050180e3", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Consumer by id

        @param str id
        @return Consumer of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("7dde0a74-bf80-4bd8-aa64-9603f9b368af", Consumer(mapObj))


    def delete(self):
        """
        Delete object of type Consumer

        @return Consumer of the response of the deleted instance.
        """
        return BaseObject.execute("7dde0a74-bf80-4bd8-aa64-9603f9b368af", self)




