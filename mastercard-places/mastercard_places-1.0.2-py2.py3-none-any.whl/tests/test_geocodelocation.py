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


class GeocodeLocationTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_geocode_location(self):
        

        
    
        map = RequestMap()
        map.set("addressLine1", "2254 HIGHWAY K")
        map.set("cityName", "O FALLON")
        map.set("countryCode", "USA")
        map.set("postalCode", "63368")
        
        
        response = GeocodeLocation.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.inputAddressLine1", response.get("geoCodeLocation.inputAddressLine1"),"2254 HIGHWAY K")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.responseAddressLine1", response.get("geoCodeLocation.responseAddressLine1"),"2254 HIGHWAY K")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.inputCityName", response.get("geoCodeLocation.inputCityName"),"O FALLON")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.responseCityName", response.get("geoCodeLocation.responseCityName"),"O FALLON")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.responseCountrySubDivision", response.get("geoCodeLocation.responseCountrySubDivision"),"MO")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.inputCountryCode", response.get("geoCodeLocation.inputCountryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.responseCountryCode", response.get("geoCodeLocation.responseCountryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.inputPostalCode", response.get("geoCodeLocation.inputPostalCode"),"63368")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.responsePostalCode", response.get("geoCodeLocation.responsePostalCode"),"63368-7929")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.latitude", response.get("geoCodeLocation.latitude"),"38.777414")
        self.customAssertEqual(ignoreAsserts, "geoCodeLocation.longitude", response.get("geoCodeLocation.longitude"),"-90.699736")
        

        BaseTest.putResponse("example_geocode_location", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

