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


class SpendingPulseReportTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_spendingpulse(self):
        

        
    
        map = RequestMap()
        map.set("CurrentRow", "1")
        map.set("Offset", "25")
        map.set("ProductLine", "Weekly Sales")
        map.set("PublicationCoveragePeriod", "Week")
        map.set("Country", "US")
        map.set("ReportType", "reportA")
        map.set("Period", "Weekly")
        map.set("Sector", "sectorA")
        map.set("Ecomm", "Y")
        
        
        response = SpendingPulseReport.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.Count", response.get("SpendingPulseList.Count"),"2")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.Message", response.get("SpendingPulseList.Message"),"Success")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Country", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].CurrencyOfForSalesValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].CurrencyOfForSalesValue"),"US Dollars")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Ecomm", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Ecomm"),"Y")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ImpliedDeflatorMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ImpliedDeflatorMonthOverMonthChange"),"0.0012")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ImpliedDeflatorYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ImpliedDeflatorYearOverYearChange"),"0.0011")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].NonGregorianReportingPeriod", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].NonGregorianReportingPeriod"),"2015-05")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Period", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Period"),"Weekly")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PeriodEndDate", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PeriodEndDate"),"5/14/2015")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PeriodStartDate", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PeriodStartDate"),"5/8/2015")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceAdjustmentFlag", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceAdjustmentFlag"),"Y")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndex3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndex3MonthMovingAverageChange"),"0.012")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexMonthOverMonthChange"),"0.005")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexValue"),"0.00115")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexYearOverYearChange"),"0.00115")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ProductLine", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ProductLine"),"Weekly Sales")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PublicationCoveragePeriod", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ReportType", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ReportType"),"reportA")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ReportingCalender", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ReportingCalender"),"G")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Sales3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Sales3MonthMovingAverageChange"),"150")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesMonthOverMonthChange"),"50")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesValueIndex", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesValueIndex"),"5")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesYearOverYearChange"),"500")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesYearToDateChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesYearToDateChange"),"20")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SameStoreSalesIndex3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SameStoreSalesIndex3MonthMovingAverageChange"),"0.68")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SameStoreSalesIndexYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SameStoreSalesIndexYearOverYearChange"),"0.6")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SeasonalAdjustmentFlag", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SeasonalAdjustmentFlag"),"Y")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Sector", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Sector"),"sectorA")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Segment", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Segment"),"seg1")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SubGeographyValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SubGeographyValue"),"region")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SubSector", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SubSector"),"subA")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndex3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndex3MonthMovingAverageChange"),"0.58")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexMonthOverMonthChange"),"0.57")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexValue"),"0.5")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexYearOverYearChange"),"0.56")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Country", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].CurrencyOfForSalesValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].CurrencyOfForSalesValue"),"US Dollars")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Ecomm", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Ecomm"),"Y")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ImpliedDeflatorMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ImpliedDeflatorMonthOverMonthChange"),"0.0012")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ImpliedDeflatorYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ImpliedDeflatorYearOverYearChange"),"0.0011")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].NonGregorianReportingPeriod", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].NonGregorianReportingPeriod"),"2015-05")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Period", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Period"),"Weekly")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PeriodEndDate", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PeriodEndDate"),"5/7/2015")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PeriodStartDate", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PeriodStartDate"),"5/1/2015")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceAdjustmentFlag", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceAdjustmentFlag"),"Y")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndex3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndex3MonthMovingAverageChange"),"0.013")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexMonthOverMonthChange"),"0.006")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexValue"),"0.000116")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexYearOverYearChange"),"0.00116")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ProductLine", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ProductLine"),"Weekly Sales")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PublicationCoveragePeriod", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ReportType", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ReportType"),"reportA")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ReportingCalender", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ReportingCalender"),"G")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Sales3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Sales3MonthMovingAverageChange"),"160")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesMonthOverMonthChange"),"60")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesValueIndex", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesValueIndex"),"6")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesYearOverYearChange"),"600")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesYearToDateChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesYearToDateChange"),"30")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SameStoreSalesIndex3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SameStoreSalesIndex3MonthMovingAverageChange"),"0.88")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SameStoreSalesIndexYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SameStoreSalesIndexYearOverYearChange"),"0.8")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SeasonalAdjustmentFlag", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SeasonalAdjustmentFlag"),"Y")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Sector", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Sector"),"sectorA")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Segment", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Segment"),"seg1")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SubGeographyValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SubGeographyValue"),"region")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SubSector", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SubSector"),"subA")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndex3MonthMovingAverageChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndex3MonthMovingAverageChange"),"0.48")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexMonthOverMonthChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexMonthOverMonthChange"),"0.47")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexValue", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexValue"),"0.4")
        self.customAssertEqual(ignoreAsserts, "SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexYearOverYearChange", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexYearOverYearChange"),"0.46")
        

        BaseTest.putResponse("example_spendingpulse", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

