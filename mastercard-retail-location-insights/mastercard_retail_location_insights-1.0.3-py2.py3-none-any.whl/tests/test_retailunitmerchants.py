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


class RetailUnitMerchantsTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_retail_unit_merchants(self):
        

        
    
        map = RequestMap()
        map.set("PageOffset", "1")
        map.set("PageLength", "100")
        map.set("RetailUnitType", "State")
        map.set("RetailUnitId", "4")
        
        
        response = RetailUnitMerchants.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.PageOffset", response.get("RetailUnitMerchantResponse.PageOffset"),"1")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.TotalCount", response.get("RetailUnitMerchantResponse.TotalCount"),"12")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Period", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Period"),"2016/03")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].RetailUnit.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].RetailUnit.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Id", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Id"),"74")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Name", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Name"),"PROFIX SERVICE CTR")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.ChannelOfDistribution", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.ChannelOfDistribution"),"B")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Industry", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Industry"),"MRS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.IndustryName", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.IndustryName"),"Maintenance and Repair Se")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.StreetAddress", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.StreetAddress"),"96 THE PARADE")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.City", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.City"),"NORWOOD")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.PostalCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.PostalCode"),"5067")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.CountrySubdivision", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.CountrySubdivision"),"SA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Latitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Latitude"),"-34.921538")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Longitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Longitude"),"138.631115")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Period", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Period"),"2016/03")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].RetailUnit.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].RetailUnit.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Id", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Id"),"75")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Name", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Name"),"DR DAVID CARMAN")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.ChannelOfDistribution", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.ChannelOfDistribution"),"B")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Industry", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Industry"),"HCS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.IndustryName", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.IndustryName"),"Health Care and Social As")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.StreetAddress", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.StreetAddress"),"48 KING WILLIAM ROAD")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.City", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.City"),"GOODWOOD")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.PostalCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.PostalCode"),"5034")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.CountrySubdivision", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.CountrySubdivision"),"SA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Latitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Latitude"),"-34.948616")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Longitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Longitude"),"138.599496")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Period", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Period"),"2016/03")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].RetailUnit.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].RetailUnit.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Id", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Id"),"76")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Name", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Name"),"SUNRISE CHILDREN ASSO")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.ChannelOfDistribution", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.ChannelOfDistribution"),"C")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Industry", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Industry"),"RCP")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.IndustryName", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.IndustryName"),"Religious")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.StreetAddress", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.StreetAddress"),"46 A ST ANNS PLACE")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.City", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.City"),"PARKSIDE")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.PostalCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.PostalCode"),"5063")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.CountrySubdivision", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.CountrySubdivision"),"SA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Latitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Latitude"),"-34.942697")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Longitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Longitude"),"138.615377")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Period", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Period"),"2016/03")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].RetailUnit.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].RetailUnit.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Id", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Id"),"77")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Name", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Name"),"BEST BUY MOTORS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.ChannelOfDistribution", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.ChannelOfDistribution"),"B")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Industry", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Industry"),"AUC")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.IndustryName", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.IndustryName"),"Automotive Used Only Car ")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.StreetAddress", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.StreetAddress"),"232 HAMPSTEAD ROAD")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.City", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.City"),"CLEARVIEW")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.PostalCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.PostalCode"),"5085")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.CountrySubdivision", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.CountrySubdivision"),"SA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.CountryCode", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Latitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Latitude"),"-34.860851")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Longitude", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Longitude"),"138.618136")
        

        BaseTest.putResponse("example_retail_unit_merchants", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

