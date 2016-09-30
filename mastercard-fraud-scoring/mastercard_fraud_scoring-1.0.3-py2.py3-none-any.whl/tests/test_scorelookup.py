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
from mastercardfraudscoring import *


class ScoreLookupTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
                
    def test_example_score(self):
        

        
    
        map = RequestMap()
        map.set("ScoreLookupRequest.TransactionDetail.CustomerIdentifier", "1996")
        map.set("ScoreLookupRequest.TransactionDetail.MerchantIdentifier", "12345")
        map.set("ScoreLookupRequest.TransactionDetail.AccountNumber", "5555555555555555")
        map.set("ScoreLookupRequest.TransactionDetail.AccountPrefix", "555555")
        map.set("ScoreLookupRequest.TransactionDetail.AccountSuffix", "5555")
        map.set("ScoreLookupRequest.TransactionDetail.TransactionAmount", "12500")
        map.set("ScoreLookupRequest.TransactionDetail.TransactionDate", "1231")
        map.set("ScoreLookupRequest.TransactionDetail.TransactionTime", "035931")
        map.set("ScoreLookupRequest.TransactionDetail.BankNetReferenceNumber", "abc123hij")
        map.set("ScoreLookupRequest.TransactionDetail.Stan", "123456")
        
        
        response = ScoreLookup(map).update()

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.CustomerIdentifier", response.get("ScoreLookup.CustomerIdentifier"),"L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.CustomerIdentifier", response.get("ScoreLookup.TransactionDetail.CustomerIdentifier"),"1996")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.MerchantIdentifier", response.get("ScoreLookup.TransactionDetail.MerchantIdentifier"),"12345")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.AccountNumber", response.get("ScoreLookup.TransactionDetail.AccountNumber"),"5555555555555555")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.AccountPrefix", response.get("ScoreLookup.TransactionDetail.AccountPrefix"),"555555")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.AccountSuffix", response.get("ScoreLookup.TransactionDetail.AccountSuffix"),"5555")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.TransactionAmount", response.get("ScoreLookup.TransactionDetail.TransactionAmount"),"12500")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.TransactionDate", response.get("ScoreLookup.TransactionDetail.TransactionDate"),"1231")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.TransactionTime", response.get("ScoreLookup.TransactionDetail.TransactionTime"),"035931")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.BankNetReferenceNumber", response.get("ScoreLookup.TransactionDetail.BankNetReferenceNumber"),"abc123hij")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.TransactionDetail.Stan", response.get("ScoreLookup.TransactionDetail.Stan"),"123456")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.ScoreResponse.MatchIndicator", response.get("ScoreLookup.ScoreResponse.MatchIndicator"),"2")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.ScoreResponse.FraudScore", response.get("ScoreLookup.ScoreResponse.FraudScore"),"681")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.ScoreResponse.ReasonCode", response.get("ScoreLookup.ScoreResponse.ReasonCode"),"A5")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.ScoreResponse.RulesAdjustedScore", response.get("ScoreLookup.ScoreResponse.RulesAdjustedScore"),"701")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.ScoreResponse.RulesAdjustedReasonCode", response.get("ScoreLookup.ScoreResponse.RulesAdjustedReasonCode"),"19")
        self.customAssertEqual(ignoreAsserts, "ScoreLookup.ScoreResponse.RulesAdjustedReasonCodeSecondary", response.get("ScoreLookup.ScoreResponse.RulesAdjustedReasonCodeSecondary"),"A9")
        

        BaseTest.putResponse("example_score", response)
        

    
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

