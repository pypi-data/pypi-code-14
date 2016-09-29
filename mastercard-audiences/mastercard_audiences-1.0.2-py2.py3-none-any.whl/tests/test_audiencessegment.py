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
from mastercardaudiences import *


class AudiencesSegmentTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_audience_request(self):
        

        
    
        map = RequestMap()
        map.set("PageLength", "10")
        map.set("PageOffset", "1")
        map.set("ZipRangeStart", "000000000")
        map.set("ZipRangeEnd", "999999999")
        map.set("Segment", "Standard_000001")
        map.set("DecileIDRangeStart", "1")
        map.set("DecileIDRangeEnd", "20")
        
        
        response = AudiencesSegment.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "Response.PageOffset", response.get("Response.PageOffset"),"1")
        self.customAssertEqual(ignoreAsserts, "Response.TotalCount", response.get("Response.TotalCount"),"98")
        self.customAssertEqual(ignoreAsserts, "Response.ArrayOfAudience[0].Audience.Zip", response.get("Response.ArrayOfAudience[0].Audience.Zip"),"311125860")
        self.customAssertEqual(ignoreAsserts, "Response.ArrayOfAudience[0].Audience.Segment", response.get("Response.ArrayOfAudience[0].Audience.Segment"),"Standard_000001")
        self.customAssertEqual(ignoreAsserts, "Response.ArrayOfAudience[0].Audience.Demidecile", response.get("Response.ArrayOfAudience[0].Audience.Demidecile"),"20")
        

        BaseTest.putResponse("example_audience_request", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

