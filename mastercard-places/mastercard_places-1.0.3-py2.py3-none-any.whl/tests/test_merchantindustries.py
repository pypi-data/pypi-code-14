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


class MerchantIndustriesTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_merchantindustries(self):
        

        
    
        map = RequestMap()
        map.set("Ind_Codes", "true")
        
        
        response = MerchantIndustries.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[0].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[0].Industry"),"AAC")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[0].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[0].IndustryName"),"Children's Apparel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[1].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[1].Industry"),"AAF")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[1].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[1].IndustryName"),"Family Apparel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[2].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[2].Industry"),"ACC")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[2].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[2].IndustryName"),"Accommodations")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[3].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[3].Industry"),"ACS")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[3].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[3].IndustryName"),"Automotive New and Used Car Sales")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[4].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[4].Industry"),"ADV")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[4].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[4].IndustryName"),"Advertising Services")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[5].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[5].Industry"),"AFH")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[5].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[5].IndustryName"),"Agriculture/Forestry/Fishing/Hunting")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[6].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[6].Industry"),"AFS")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[6].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[6].IndustryName"),"Automotive Fuel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[7].Industry", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[7].Industry"),"ALS")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[7].IndustryName", response.get("MerchantIndustryList.MerchantIndustryArray.MerchantIndustry[7].IndustryName"),"Accounting and Legal Services")
        

        BaseTest.putResponse("example_merchantindustries", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

