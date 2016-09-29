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
from mastercardspendingpulse import *


class ParametersTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_parameters(self):
        

        
    
        map = RequestMap()
        map.set("CurrentRow", "1")
        map.set("Offset", "25")
        
        
        response = Parameters.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "ParameterList.Count", response.get("ParameterList.Count"),"4")
        self.customAssertEqual(ignoreAsserts, "ParameterList.Message", response.get("ParameterList.Message"),"Success")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[0].Country", response.get("ParameterList.ParameterArray.Parameter[0].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[0].Ecomm", response.get("ParameterList.ParameterArray.Parameter[0].Ecomm"),"Y")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[0].Period", response.get("ParameterList.ParameterArray.Parameter[0].Period"),"Weekly")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[0].ProductLine", response.get("ParameterList.ParameterArray.Parameter[0].ProductLine"),"US Gasoline Weekly")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[0].PublicationCoveragePeriod", response.get("ParameterList.ParameterArray.Parameter[0].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[0].ReportType", response.get("ParameterList.ParameterArray.Parameter[0].ReportType"),"Gas")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[0].Sector", response.get("ParameterList.ParameterArray.Parameter[0].Sector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[1].Country", response.get("ParameterList.ParameterArray.Parameter[1].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[1].Ecomm", response.get("ParameterList.ParameterArray.Parameter[1].Ecomm"),"Y")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[1].Period", response.get("ParameterList.ParameterArray.Parameter[1].Period"),"Monthly")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[1].ProductLine", response.get("ParameterList.ParameterArray.Parameter[1].ProductLine"),"US Gasoline Monthly")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[1].PublicationCoveragePeriod", response.get("ParameterList.ParameterArray.Parameter[1].PublicationCoveragePeriod"),"Month")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[1].ReportType", response.get("ParameterList.ParameterArray.Parameter[1].ReportType"),"Gas")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[1].Sector", response.get("ParameterList.ParameterArray.Parameter[1].Sector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[2].Country", response.get("ParameterList.ParameterArray.Parameter[2].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[2].Ecomm", response.get("ParameterList.ParameterArray.Parameter[2].Ecomm"),"Y")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[2].Period", response.get("ParameterList.ParameterArray.Parameter[2].Period"),"Weekly")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[2].ProductLine", response.get("ParameterList.ParameterArray.Parameter[2].ProductLine"),"Weekly Sales")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[2].PublicationCoveragePeriod", response.get("ParameterList.ParameterArray.Parameter[2].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[2].ReportType", response.get("ParameterList.ParameterArray.Parameter[2].ReportType"),"reportA")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[2].Sector", response.get("ParameterList.ParameterArray.Parameter[2].Sector"),"sectorA")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[3].Country", response.get("ParameterList.ParameterArray.Parameter[3].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[3].Ecomm", response.get("ParameterList.ParameterArray.Parameter[3].Ecomm"),"Y")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[3].Period", response.get("ParameterList.ParameterArray.Parameter[3].Period"),"Weekly")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[3].ProductLine", response.get("ParameterList.ParameterArray.Parameter[3].ProductLine"),"Weekly Sales")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[3].PublicationCoveragePeriod", response.get("ParameterList.ParameterArray.Parameter[3].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[3].ReportType", response.get("ParameterList.ParameterArray.Parameter[3].ReportType"),"reportB")
        self.customAssertEqual(ignoreAsserts, "ParameterList.ParameterArray.Parameter[3].Sector", response.get("ParameterList.ParameterArray.Parameter[3].Sector"),"sectorB")
        

        BaseTest.putResponse("example_parameters", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

