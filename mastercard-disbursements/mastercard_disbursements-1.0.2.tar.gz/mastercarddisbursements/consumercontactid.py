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
        "69ed0b87-230f-4162-a36d-ec0d0346d81d" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "query", [], []),
        "94b51039-13a2-49f9-bc80-82ab28f054dc" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids", "create", [], []),
        "0819a10f-63d0-4cb1-9c1d-663ba117fe50" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "read", [], []),
        "991c464a-a250-4d88-8989-32a1fab52085" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "update", [], []),
        "764cf476-0146-4986-a398-ddd2697325dd" : OperationConfig("/send/v1/partners/{partnerId}/consumers/{consumerId}/contact_ids/{contactId}", "delete", [], []),
        
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

        return BaseObject.execute("69ed0b87-230f-4162-a36d-ec0d0346d81d", ConsumerContactID(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type ConsumerContactID

        @param Dict mapObj, containing the required parameters to create a new object
        @return ConsumerContactID of the response of created instance.
        """
        return BaseObject.execute("94b51039-13a2-49f9-bc80-82ab28f054dc", ConsumerContactID(mapObj))











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

        return BaseObject.execute("0819a10f-63d0-4cb1-9c1d-663ba117fe50", ConsumerContactID(mapObj))



    def update(self):
        """
        Updates an object of type ConsumerContactID

        @return ConsumerContactID object representing the response.
        """
        return BaseObject.execute("991c464a-a250-4d88-8989-32a1fab52085", self)








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

        return BaseObject.execute("764cf476-0146-4986-a398-ddd2697325dd", ConsumerContactID(mapObj))


    def delete(self):
        """
        Delete object of type ConsumerContactID

        @return ConsumerContactID of the response of the deleted instance.
        """
        return BaseObject.execute("764cf476-0146-4986-a398-ddd2697325dd", self)




