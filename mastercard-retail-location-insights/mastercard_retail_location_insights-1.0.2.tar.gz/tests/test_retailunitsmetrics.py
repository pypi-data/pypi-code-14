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


class RetailUnitsMetricsTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_retail_unit_metrics(self):
        

        
    
        map = RequestMap()
        map.set("PageOffset", "1")
        map.set("PageLength", "10")
        map.set("RetailUnitType", "State")
        map.set("RetailUnitId", "4")
        
        
        response = RetailUnitsMetrics.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.PageOffset", response.get("RetailUnitMetricResponse.PageOffset"),"1")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.TotalCount", response.get("RetailUnitMetricResponse.TotalCount"),"4")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RetailUnitId", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RetailUnitId"),"4")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RetailUnitType", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RetailUnitType"),"STATE")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].Period", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].Period"),"2016/03")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.CompositeIndustry", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.CompositeIndustry"),"100")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.CompositeIndustryName", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.CompositeIndustryName"),"All Retail")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Sales", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Sales"),"500")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Transactions", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Transactions"),"500")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.TicketSize", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.TicketSize"),"300")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Growth", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Growth"),"700")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Stability", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Stability"),"600")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Composite", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Composite"),"400")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RetailUnitId", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RetailUnitId"),"4")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RetailUnitType", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RetailUnitType"),"STATE")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].Period", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].Period"),"2016/03")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.CompositeIndustry", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.CompositeIndustry"),"102")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.CompositeIndustryName", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.CompositeIndustryName"),"Eating Places")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Sales", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Sales"),"445")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Transactions", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Transactions"),"445")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.TicketSize", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.TicketSize"),"334")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Growth", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Growth"),"556")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Stability", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Stability"),"556")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Composite", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Composite"),"445")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RetailUnitId", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RetailUnitId"),"4")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RetailUnitType", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RetailUnitType"),"STATE")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].Period", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].Period"),"2016/03")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.CompositeIndustry", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.CompositeIndustry"),"103")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.CompositeIndustryName", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.CompositeIndustryName"),"Exclude Eating")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Sales", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Sales"),"500")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Transactions", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Transactions"),"500")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.TicketSize", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.TicketSize"),"300")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Growth", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Growth"),"700")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Stability", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Stability"),"600")
        self.customAssertEqual(ignoreAsserts, "RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Composite", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Composite"),"400")
        

        BaseTest.putResponse("example_retail_unit_metrics", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

