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


class Crossborder(BaseObject):
    """
    
    """

    __config = {
        "1ef75107-8056-4a7f-a291-d93385733494" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/crossborder", "query", [], []),
        "ef527433-daae-4dc2-98be-ea4680eae792" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/crossborder", "create", [], []),
        "73fe92d3-445b-4ad7-91c7-3a762b09e293" : OperationConfig("/issuer/v1/card/{uuid}/controls/alerts/crossborder", "delete", [], []),
        
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
        Query objects of type Crossborder by id and optional criteria
        @param type criteria
        @return Crossborder object representing the response.
        """

        return BaseObject.execute("1ef75107-8056-4a7f-a291-d93385733494", Crossborder(criteria))


    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type Crossborder

        @param Dict mapObj, containing the required parameters to create a new object
        @return Crossborder of the response of created instance.
        """
        return BaseObject.execute("ef527433-daae-4dc2-98be-ea4680eae792", Crossborder(mapObj))









    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type Crossborder by id

        @param str id
        @return Crossborder of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("73fe92d3-445b-4ad7-91c7-3a762b09e293", Crossborder(mapObj))


    def delete(self):
        """
        Delete object of type Crossborder

        @return Crossborder of the response of the deleted instance.
        """
        return BaseObject.execute("73fe92d3-445b-4ad7-91c7-3a762b09e293", self)




