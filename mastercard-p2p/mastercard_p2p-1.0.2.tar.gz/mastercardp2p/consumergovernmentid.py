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
        "1b4daa94-56fd-489d-9da8-e074513482dd" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "query", [], []),
        "da10ab4e-4094-4b74-a9e6-f7398e8dfb0d" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids", "create", [], []),
        "fdc9ddd7-93e7-4b58-bd9d-2484e907d027" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "read", [], []),
        "ae227b1c-5495-4fda-aee3-53f016cb28a1" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "update", [], []),
        "4e1f0b88-bbbf-472c-aacb-6eb0b42115d5" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/government_ids/{governmentId}", "delete", [], []),
        
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

        return BaseObject.execute("1b4daa94-56fd-489d-9da8-e074513482dd", ConsumerGovernmentID(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ConsumerGovernmentID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerGovernmentID of the response of created instance.
        """
        return BaseObject.execute("da10ab4e-4094-4b74-a9e6-f7398e8dfb0d", ConsumerGovernmentID(mapObj))











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

        return BaseObject.execute("fdc9ddd7-93e7-4b58-bd9d-2484e907d027", ConsumerGovernmentID(mapObj))



    def update(self):
        """
        Updates an object of type ConsumerGovernmentID

        @return ConsumerGovernmentID object representing the response.
        """
        return BaseObject.execute("ae227b1c-5495-4fda-aee3-53f016cb28a1", self)








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

        return BaseObject.execute("4e1f0b88-bbbf-472c-aacb-6eb0b42115d5", ConsumerGovernmentID(mapObj))


    def delete(self):
        """
        Delete object of type ConsumerGovernmentID

        @return ConsumerGovernmentID of the response of the deleted instance.
        """
        return BaseObject.execute("4e1f0b88-bbbf-472c-aacb-6eb0b42115d5", self)




