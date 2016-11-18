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


class Channel(BaseObject):
    """
    
    """

    __config = {
        "25c4260c-21d5-4478-ada6-10be1eb5cc96" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/channels", "query", [], []),
        "5097403c-d40d-46c1-8d0d-2359bdd7f0f6" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/channels", "create", [], []),
        "4e6e8365-a7f3-4cc3-acb2-b2a59008e99b" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/channels", "delete", [], []),
        
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
        Query objects of type Channel by id and optional criteria
        @param type criteria
        @return Channel object representing the response.
        """

        return BaseObject.execute("25c4260c-21d5-4478-ada6-10be1eb5cc96", Channel(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Channel

        @param Dict mapObj, containing the required parameters to create a new object
        @return Channel of the response of created instance.
        """
        return BaseObject.execute("5097403c-d40d-46c1-8d0d-2359bdd7f0f6", Channel(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Channel by id

        @param str id
        @return Channel of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("4e6e8365-a7f3-4cc3-acb2-b2a59008e99b", Channel(mapObj))


    def delete(self):
        """
        Delete object of type Channel

        @return Channel of the response of the deleted instance.
        """
        return BaseObject.execute("4e6e8365-a7f3-4cc3-acb2-b2a59008e99b", self)




