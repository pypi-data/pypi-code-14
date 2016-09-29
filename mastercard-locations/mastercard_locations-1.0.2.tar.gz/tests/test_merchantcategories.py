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


class MerchantCategoriesTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_merchants_category(self):
        

        
    
        map = RequestMap()
        
        
        response = MerchantCategories.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "Categories.Category[0]", response.get("Categories.Category[0]"),"1Apparel")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[1]", response.get("Categories.Category[1]"),"2Automotive")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[2]", response.get("Categories.Category[2]"),"3Beauty")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[3]", response.get("Categories.Category[3]"),"4Book Stores")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[4]", response.get("Categories.Category[4]"),"5Convenience Stores")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[5]", response.get("Categories.Category[5]"),"7Dry Cleaners And Laundry Services")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[6]", response.get("Categories.Category[6]"),"8Fast Food Restaurants")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[7]", response.get("Categories.Category[7]"),"9Gift Shops, Hobbies, Jewelers")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[8]", response.get("Categories.Category[8]"),"10Grocery Stores And Supermarkets")
        self.customAssertEqual(ignoreAsserts, "Categories.Category[9]", response.get("Categories.Category[9]"),"11Health")
        

        BaseTest.putResponse("example_merchants_category", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

