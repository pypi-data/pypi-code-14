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


class ATMLocationsTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_atm_locations(self):
        

        
    
        map = RequestMap()
        map.set("PageOffset", "0")
        map.set("PageLength", "5")
        map.set("PostalCode", "11101")
        
        
        response = ATMLocations.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "Atms.PageOffset", response.get("Atms.PageOffset"),"0")
        self.customAssertEqual(ignoreAsserts, "Atms.TotalCount", response.get("Atms.TotalCount"),"26")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Name", response.get("Atms.Atm[0].Location.Name"),"Sandbox ATM Location 1")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Distance", response.get("Atms.Atm[0].Location.Distance"),"0.9320591049747101")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.DistanceUnit", response.get("Atms.Atm[0].Location.DistanceUnit"),"MILE")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Address.Line1", response.get("Atms.Atm[0].Location.Address.Line1"),"4201 Leverton Cove Road")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Address.City", response.get("Atms.Atm[0].Location.Address.City"),"SPRINGFIELD")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Address.PostalCode", response.get("Atms.Atm[0].Location.Address.PostalCode"),"11101")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Address.CountrySubdivision.Name", response.get("Atms.Atm[0].Location.Address.CountrySubdivision.Name"),"UYQQQQ")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Address.CountrySubdivision.Code", response.get("Atms.Atm[0].Location.Address.CountrySubdivision.Code"),"QQ")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Address.Country.Name", response.get("Atms.Atm[0].Location.Address.Country.Name"),"UYQQQRR")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Address.Country.Code", response.get("Atms.Atm[0].Location.Address.Country.Code"),"UYQ")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Point.Latitude", response.get("Atms.Atm[0].Location.Point.Latitude"),"38.76006576913497")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.Point.Longitude", response.get("Atms.Atm[0].Location.Point.Longitude"),"-90.74615107952418")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Location.LocationType.Type", response.get("Atms.Atm[0].Location.LocationType.Type"),"OTHER")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].HandicapAccessible", response.get("Atms.Atm[0].HandicapAccessible"),"NO")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Camera", response.get("Atms.Atm[0].Camera"),"NO")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Availability", response.get("Atms.Atm[0].Availability"),"UNKNOWN")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].AccessFees", response.get("Atms.Atm[0].AccessFees"),"UNKNOWN")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Owner", response.get("Atms.Atm[0].Owner"),"Sandbox ATM 1")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].SharedDeposit", response.get("Atms.Atm[0].SharedDeposit"),"NO")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].SurchargeFreeAlliance", response.get("Atms.Atm[0].SurchargeFreeAlliance"),"NO")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].SurchargeFreeAllianceNetwork", response.get("Atms.Atm[0].SurchargeFreeAllianceNetwork"),"DOES_NOT_PARTICIPATE_IN_SFA")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].Sponsor", response.get("Atms.Atm[0].Sponsor"),"Sandbox")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].SupportEMV", response.get("Atms.Atm[0].SupportEMV"),"1")
        self.customAssertEqual(ignoreAsserts, "Atms.Atm[0].InternationalMaestroAccepted", response.get("Atms.Atm[0].InternationalMaestroAccepted"),"1")
        

        BaseTest.putResponse("atm_locations", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

