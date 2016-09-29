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
from mastercardretaillocationinsights import *


class MerchantIndustriesTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_merchant_industries(self):
        

        
    
        map = RequestMap()
        
        
        response = MerchantIndustries.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[0].Industry", response.get("MerchantIndustries.MerchantIndustry[0].Industry"),"AAC")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[0].IndustryName", response.get("MerchantIndustries.MerchantIndustry[0].IndustryName"),"Children's Apparel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[1].Industry", response.get("MerchantIndustries.MerchantIndustry[1].Industry"),"AAF")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[1].IndustryName", response.get("MerchantIndustries.MerchantIndustry[1].IndustryName"),"Family Apparel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[2].Industry", response.get("MerchantIndustries.MerchantIndustry[2].Industry"),"AAM")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[2].IndustryName", response.get("MerchantIndustries.MerchantIndustry[2].IndustryName"),"Men's Apparel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[3].Industry", response.get("MerchantIndustries.MerchantIndustry[3].Industry"),"AAW")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[3].IndustryName", response.get("MerchantIndustries.MerchantIndustry[3].IndustryName"),"Women's Apparel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[4].Industry", response.get("MerchantIndustries.MerchantIndustry[4].Industry"),"AAX")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[4].IndustryName", response.get("MerchantIndustries.MerchantIndustry[4].IndustryName"),"Miscellaneous Apparel")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[5].Industry", response.get("MerchantIndustries.MerchantIndustry[5].Industry"),"ACC")
        self.customAssertEqual(ignoreAsserts, "MerchantIndustries.MerchantIndustry[5].IndustryName", response.get("MerchantIndustries.MerchantIndustry[5].IndustryName"),"Accommodations")
        

        BaseTest.putResponse("example_merchant_industries", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

