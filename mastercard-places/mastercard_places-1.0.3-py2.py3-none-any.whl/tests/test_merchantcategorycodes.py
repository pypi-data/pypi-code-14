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

import unittest
import time
from mastercardapicore import RequestMap
from base_test import BaseTest
from mastercardplaces import *


class MerchantCategoryCodesTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_merchantcategorycodes(self):
        

        
    
        map = RequestMap()
        map.set("Mcc_Codes", "true")
        
        
        response = MerchantCategoryCodes.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[0].MerchantCatCode", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[0].MerchantCatCode"),"0001")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[0].MerchantCategoryName", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[0].MerchantCategoryName"),"TAP (PORTUGAL)")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[1].MerchantCatCode", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[1].MerchantCatCode"),"0002")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[1].MerchantCategoryName", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[1].MerchantCategoryName"),"ANSA INTERNATIONAL")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[2].MerchantCatCode", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[2].MerchantCatCode"),"0003")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[2].MerchantCategoryName", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[2].MerchantCategoryName"),"CARLTON HOTELS")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[3].MerchantCatCode", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[3].MerchantCatCode"),"0004")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[3].MerchantCategoryName", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[3].MerchantCategoryName"),"AIR CARRIERS  AIRLINES-NOT ELSEWHERE CLASSIFIED")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[4].MerchantCatCode", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[4].MerchantCatCode"),"0005")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[4].MerchantCategoryName", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[4].MerchantCategoryName"),"TRAVEL AGENCIES AND TOUR OPERATORS")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[5].MerchantCatCode", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[5].MerchantCatCode"),"0006")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[5].MerchantCategoryName", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[5].MerchantCategoryName"),"UTLTS-ELCTRC  GAS  HEATING OIL  SANITARY  WATER")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[6].MerchantCatCode", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[6].MerchantCatCode"),"0007")
        self.customAssertEqual(ignoreAsserts, "MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[6].MerchantCategoryName", response.get("MerchantCategoryCodeList.MerchantCategoryCodeArray.MerchantCategoryCode[6].MerchantCategoryName"),"COMPUTERS  COMPUTER PERIPHERAL EQUIPMENT  SOFTWARE")
        

        BaseTest.putResponse("example_merchantcategorycodes", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

