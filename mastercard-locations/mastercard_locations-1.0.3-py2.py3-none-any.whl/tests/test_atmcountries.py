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
from mastercardlocations import *


class ATMCountriesTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_atm_country(self):
        

        
    
        map = RequestMap()
        
        
        response = ATMCountries.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "Countries.Country[0].Name", response.get("Countries.Country[0].Name"),"THAILAND")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[0].Code", response.get("Countries.Country[0].Code"),"THA")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[0].Geocoding", response.get("Countries.Country[0].Geocoding"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[1].Name", response.get("Countries.Country[1].Name"),"TIMOR-LESTE")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[1].Code", response.get("Countries.Country[1].Code"),"TMP")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[1].Geocoding", response.get("Countries.Country[1].Geocoding"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[2].Name", response.get("Countries.Country[2].Name"),"TONGA")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[2].Code", response.get("Countries.Country[2].Code"),"TON")
        self.customAssertEqual(ignoreAsserts, "Countries.Country[2].Geocoding", response.get("Countries.Country[2].Geocoding"),"FALSE")
        

        BaseTest.putResponse("example_atm_country", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

