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


class GasWeeklyTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
        
        
        
        
        
                
    def test_example_gasweekly(self):
        

        
    
        map = RequestMap()
        map.set("CurrentRow", "1")
        map.set("Offset", "25")
        
        
        response = GasWeekly.query(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.Count", response.get("GasWeeklyList.Count"),"4")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Country", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDCode", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDCode"),"NE")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDMillionsofBarrelsSold", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDMillionsofBarrelsSold"),"5")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDPercentChangeInBarrelsFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDPercentChangeInBarrelsFromPriorWeek"),"0.001")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDPercentChangeinBarrelsfrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDPercentChangeinBarrelsfrom52WeeksAgo"),"0.002")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Period", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Period"),"Week")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].ProductLine", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].ProductLine"),"US Gasoline Weekly")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PublicationCoveragePeriod", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].ReportType", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].ReportType"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Sector", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Sector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Segment", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Segment"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].SubSector", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].SubSector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalBarrelsChangeFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalBarrelsChangeFromPriorWeek"),"5")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrels4WeekAverage", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrels4WeekAverage"),"40")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrelsDailyAverage", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrelsDailyAverage"),"15")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrelsSold", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrelsSold"),"40")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInBarrelsFrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInBarrelsFrom52WeeksAgo"),"0.005")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInBarrelsFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInBarrelsFromPriorWeek"),"0.004")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo"),"0.006")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].WeekEndDate", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].WeekEndDate"),"6/12/2015")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Country", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDCode", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDCode"),"CA")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDMillionsofBarrelsSold", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDMillionsofBarrelsSold"),"5")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDPercentChangeInBarrelsFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDPercentChangeInBarrelsFromPriorWeek"),"0.015")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDPercentChangeinBarrelsfrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDPercentChangeinBarrelsfrom52WeeksAgo"),"0.025")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Period", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Period"),"Week")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].ProductLine", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].ProductLine"),"US Gasoline Weekly")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PublicationCoveragePeriod", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].ReportType", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].ReportType"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Sector", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Sector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Segment", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Segment"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].SubSector", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].SubSector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalBarrelsChangeFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalBarrelsChangeFromPriorWeek"),"5")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrels4WeekAverage", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrels4WeekAverage"),"40")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrelsDailyAverage", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrelsDailyAverage"),"15")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrelsSold", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrelsSold"),"40")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInBarrelsFrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInBarrelsFrom52WeeksAgo"),"0.005")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInBarrelsFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInBarrelsFromPriorWeek"),"0.004")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo"),"0.006")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].WeekEndDate", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].WeekEndDate"),"6/12/2015")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Country", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Country"),"US")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDCode", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDCode"),"NE")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDMillionsofBarrelsSold", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDMillionsofBarrelsSold"),"6")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDPercentChangeInBarrelsFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDPercentChangeInBarrelsFromPriorWeek"),"0.002")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDPercentChangeinBarrelsfrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDPercentChangeinBarrelsfrom52WeeksAgo"),"0.003")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Period", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Period"),"Week")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].ProductLine", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].ProductLine"),"US Gasoline Weekly")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PublicationCoveragePeriod", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PublicationCoveragePeriod"),"Week")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].ReportType", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].ReportType"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Sector", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Sector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Segment", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Segment"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].SubSector", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].SubSector"),"Gas")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalBarrelsChangeFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalBarrelsChangeFromPriorWeek"),"6")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrels4WeekAverage", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrels4WeekAverage"),"50")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrelsDailyAverage", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrelsDailyAverage"),"16")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrelsSold", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrelsSold"),"50")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInBarrelsFrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInBarrelsFrom52WeeksAgo"),"0.006")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInBarrelsFromPriorWeek", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInBarrelsFromPriorWeek"),"0.005")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo"),"0.007")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].WeekEndDate", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].WeekEndDate"),"6/5/2015")
        self.customAssertEqual(ignoreAsserts, "GasWeeklyList.Message", response.get("GasWeeklyList.Message"),"Success")
        

        BaseTest.putResponse("example_gasweekly", response)
        

    
        
    

if __name__ == '__main__':
    unittest.main()

