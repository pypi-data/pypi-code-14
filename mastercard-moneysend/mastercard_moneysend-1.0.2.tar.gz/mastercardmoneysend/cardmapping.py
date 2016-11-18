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


class CardMapping(BaseObject):
    """
    
    """

    __config = {
        "75bb855b-3772-40ac-8031-0642c066b9b8" : OperationConfig("/moneysend/v3/mapping/card", "update", [], []),
        "6ca547e7-cf94-4800-bead-b3ace6b0e3aa" : OperationConfig("/moneysend/v3/mapping/card", "create", [], []),
        "62d4ad79-2b93-4da1-9eb8-1e6e9c7f36d6" : OperationConfig("/moneysend/v3/mapping/card/{mappingId}", "update", [], []),
        "a4da11fd-160d-4ce2-949e-c05e48cc330d" : OperationConfig("/moneysend/v3/mapping/card/{mappingId}", "delete", [], []),
        "2cc41fa6-1ccb-42ba-b323-7024e3aad5ee" : OperationConfig("/moneysend/v3/mapping/subscriber", "update", [], []),
        
    }

    def getOperationConfig(self,operationUUID):
        if operationUUID not in self.__config:
            raise Exception("Invalid operationUUID: "+operationUUI)

        return self.__config[operationUUID]

    def getOperationMetadata(self):
        return OperationMetadata(SDKConfig.getVersion(), SDKConfig.getHost())



    def read(self):
        """
        Updates an object of type CardMapping

        @return CardMapping object representing the response.
        """
        return BaseObject.execute("75bb855b-3772-40ac-8031-0642c066b9b8", self)





    @classmethod
    def create(cls,mapObj):
        """
        Creates object of type CardMapping

        @param Dict mapObj, containing the required parameters to create a new object
        @return CardMapping of the response of created instance.
        """
        return BaseObject.execute("6ca547e7-cf94-4800-bead-b3ace6b0e3aa", CardMapping(mapObj))








    def update(self):
        """
        Updates an object of type CardMapping

        @return CardMapping object representing the response.
        """
        return BaseObject.execute("62d4ad79-2b93-4da1-9eb8-1e6e9c7f36d6", self)








    @classmethod
    def deleteById(cls,id,map=None):
        """
        Delete object of type CardMapping by id

        @param str id
        @return CardMapping of the response of the deleted instance.
        """

        mapObj =  RequestMap()
        if id:
            mapObj.set("id", id)

        if map:
            if (isinstance(map,RequestMap)):
                mapObj.setAll(map.getObject())
            else:
                mapObj.setAll(map)

        return BaseObject.execute("a4da11fd-160d-4ce2-949e-c05e48cc330d", CardMapping(mapObj))


    def delete(self):
        """
        Delete object of type CardMapping

        @return CardMapping of the response of the deleted instance.
        """
        return BaseObject.execute("a4da11fd-160d-4ce2-949e-c05e48cc330d", self)





    def deleteSubscriberID(self):
        """
        Updates an object of type CardMapping

        @return CardMapping object representing the response.
        """
        return BaseObject.execute("2cc41fa6-1ccb-42ba-b323-7024e3aad5ee", self)






