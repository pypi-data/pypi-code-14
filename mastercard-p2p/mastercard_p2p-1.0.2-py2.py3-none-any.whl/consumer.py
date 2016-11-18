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
        "7299fb91-56d9-4581-b7a6-a2bdbaed662f" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "query", [], ["ref","contact_id_uri"]),
        "f7814911-4aa3-47ef-8c11-8c022000efa1" : OperationConfig("/send/v1/partners/{partnerId}/consumers", "create", [], []),
        "c2eab5bd-28fc-48ff-9f08-5d9253d8ee52" : OperationConfig("/send/v1/partners/{partnerId}/consumers/search", "create", [], []),
        "10c1be79-6a06-4a50-95ec-51476c757a91" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "read", [], []),
        "1bdf9c61-f9a1-40bb-a3ae-18bf5d2c7b7a" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "update", [], []),
        "ddc16b8f-483b-418d-b524-0e5ce97e9c14" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}", "delete", [], []),
        
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

        return BaseObject.execute("7299fb91-56d9-4581-b7a6-a2bdbaed662f", Consumer(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        """
        return BaseObject.execute("f7814911-4aa3-47ef-8c11-8c022000efa1", Consumer(mapObj))






    @classmethod
    def listByReferenceContactIDOrGovernmentID(cls,mapObj):
        """
        Creates object of type Consumer

        @param Dict mapObj, containing the required parameters to create a new object
        @return Consumer of the response of created instance.
        """
        return BaseObject.execute("c2eab5bd-28fc-48ff-9f08-5d9253d8ee52", Consumer(mapObj))











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

        return BaseObject.execute("10c1be79-6a06-4a50-95ec-51476c757a91", Consumer(mapObj))



    def update(self):
        """
        Updates an object of type Consumer

        @return Consumer object representing the response.
        """
        return BaseObject.execute("1bdf9c61-f9a1-40bb-a3ae-18bf5d2c7b7a", self)








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

        return BaseObject.execute("ddc16b8f-483b-418d-b524-0e5ce97e9c14", Consumer(mapObj))


    def delete(self):
        """
        Delete object of type Consumer

        @return Consumer of the response of the deleted instance.
        """
        return BaseObject.execute("ddc16b8f-483b-418d-b524-0e5ce97e9c14", self)




