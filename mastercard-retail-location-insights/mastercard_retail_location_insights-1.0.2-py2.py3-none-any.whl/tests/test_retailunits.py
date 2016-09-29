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


class RetailUnitsTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_retail_units(self):
        

        
    
        map = RequestMap()
        map.set("PageOffset", "1")
        map.set("PageLength", "10")
        map.set("StateId", "4")
        
        
        response = RetailUnits.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.PageOffset", response.get("RetailUnitResponse.PageOffset"),"1")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.TotalCount", response.get("RetailUnitResponse.TotalCount"),"12")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[0].CountryCode", response.get("RetailUnitResponse.RetailUnits.RetailUnit[0].CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[0].CountryName", response.get("RetailUnitResponse.RetailUnits.RetailUnit[0].CountryName"),"AUSTRALIA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[0].State", response.get("RetailUnitResponse.RetailUnits.RetailUnit[0].State"),"4")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[1].CountryCode", response.get("RetailUnitResponse.RetailUnits.RetailUnit[1].CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[1].CountryName", response.get("RetailUnitResponse.RetailUnits.RetailUnit[1].CountryName"),"AUSTRALIA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[1].State", response.get("RetailUnitResponse.RetailUnits.RetailUnit[1].State"),"4")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[2].CountryCode", response.get("RetailUnitResponse.RetailUnits.RetailUnit[2].CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[2].CountryName", response.get("RetailUnitResponse.RetailUnits.RetailUnit[2].CountryName"),"AUSTRALIA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[2].State", response.get("RetailUnitResponse.RetailUnits.RetailUnit[2].State"),"4")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[3].CountryCode", response.get("RetailUnitResponse.RetailUnits.RetailUnit[3].CountryCode"),"AUS")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[3].CountryName", response.get("RetailUnitResponse.RetailUnits.RetailUnit[3].CountryName"),"AUSTRALIA")
        self.customAssertEqual(ignoreAsserts, "RetailUnitResponse.RetailUnits.RetailUnit[3].State", response.get("RetailUnitResponse.RetailUnits.RetailUnit[3].State"),"4")
        

        BaseTest.putResponse("example_retail_units", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

