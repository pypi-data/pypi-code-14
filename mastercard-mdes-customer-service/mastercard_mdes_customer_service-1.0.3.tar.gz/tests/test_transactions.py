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
from mastercardmdescustomerservice import *


class TransactionsTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
                
    def test_example_mdes_transactions(self):
        

        
    
        map = RequestMap()
        map.set("TransactionsRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        map.set("TransactionsRequest.AuditInfo.UserId", "A1435477")
        map.set("TransactionsRequest.AuditInfo.UserName", "John Smith")
        map.set("TransactionsRequest.AuditInfo.Organization", "Any Bank")
        map.set("TransactionsRequest.AuditInfo.Phone", "5555551234")
        
        
        response = Transactions.create(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].CurrencyCode", response.get("TransactionsResponse.Transactions.Transaction[0].CurrencyCode"),"USD")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].TransactionAmount", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionAmount"),"123.45")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].TransactionTypeCode", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionTypeCode"),"PURCH")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].TransactionTypeDescription", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionTypeDescription"),"Purchase")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].TransactionStatusCode", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionStatusCode"),"AUTH")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].MerchantName", response.get("TransactionsResponse.Transactions.Transaction[0].MerchantName"),"FOODMART")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].MerchantCategoryCode", response.get("TransactionsResponse.Transactions.Transaction[0].MerchantCategoryCode"),"1234")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].MerchantCategoryDescription", response.get("TransactionsResponse.Transactions.Transaction[0].MerchantCategoryDescription"),"GROCERY STORES, SUPERMARKETS")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[0].POSEntryMode", response.get("TransactionsResponse.Transactions.Transaction[0].POSEntryMode"),"90")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].CurrencyCode", response.get("TransactionsResponse.Transactions.Transaction[1].CurrencyCode"),"USD")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].TransactionAmount", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionAmount"),"29.47")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].TransactionTypeCode", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionTypeCode"),"PURCB")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].TransactionTypeDescription", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionTypeDescription"),"Purchase with Cashback")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].TransactionStatusCode", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionStatusCode"),"COMP")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].MerchantName", response.get("TransactionsResponse.Transactions.Transaction[1].MerchantName"),"RXMART")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].MerchantCategoryCode", response.get("TransactionsResponse.Transactions.Transaction[1].MerchantCategoryCode"),"5678")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].MerchantCategoryDescription", response.get("TransactionsResponse.Transactions.Transaction[1].MerchantCategoryDescription"),"DRUG STORES, PHARMACIES")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[1].POSEntryMode", response.get("TransactionsResponse.Transactions.Transaction[1].POSEntryMode"),"91")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].CurrencyCode", response.get("TransactionsResponse.Transactions.Transaction[2].CurrencyCode"),"USD")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].TransactionAmount", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionAmount"),"-16.30")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].TransactionTypeCode", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionTypeCode"),"REFND")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].TransactionTypeDescription", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionTypeDescription"),"Refund")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].TransactionStatusCode", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionStatusCode"),"COMP")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].MerchantName", response.get("TransactionsResponse.Transactions.Transaction[2].MerchantName"),"AUTOMART")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].MerchantCategoryCode", response.get("TransactionsResponse.Transactions.Transaction[2].MerchantCategoryCode"),"9012")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].MerchantCategoryDescription", response.get("TransactionsResponse.Transactions.Transaction[2].MerchantCategoryDescription"),"AUTOMOTIVE PARTS, ACCESSORIES STORES")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[2].POSEntryMode", response.get("TransactionsResponse.Transactions.Transaction[2].POSEntryMode"),"07")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].CurrencyCode", response.get("TransactionsResponse.Transactions.Transaction[3].CurrencyCode"),"USD")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].TransactionAmount", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionAmount"),"41.89")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].TransactionTypeCode", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionTypeCode"),"AFD")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].TransactionTypeDescription", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionTypeDescription"),"Purchase Pre-Auth AFD")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].TransactionStatusCode", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionStatusCode"),"PAUTC")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].MerchantName", response.get("TransactionsResponse.Transactions.Transaction[3].MerchantName"),"GASMART")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].MerchantCategoryCode", response.get("TransactionsResponse.Transactions.Transaction[3].MerchantCategoryCode"),"3456")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].MerchantCategoryDescription", response.get("TransactionsResponse.Transactions.Transaction[3].MerchantCategoryDescription"),"FUEL DISPENSER, AUTOMATED")
        self.customAssertEqual(ignoreAsserts, "TransactionsResponse.Transactions.Transaction[3].POSEntryMode", response.get("TransactionsResponse.Transactions.Transaction[3].POSEntryMode"),"90")
        

        BaseTest.putResponse("example_mdes_transactions", response)
        

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

