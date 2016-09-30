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


class MerchantPointOfInterestTest(BaseTest):

    def setUp(self):
        Config.setDebug(True)
        self.resetAuthentication()

    
        
                
    def test_example_merchantpoi(self):
        

        
    
        map = RequestMap()
        map.set("pageOffset", "0")
        map.set("pageLength", "10")
        map.set("radiusSearch", "false")
        map.set("unit", "km")
        map.set("distance", "14")
        map.set("place.countryCode", "USA")
        
        
        response = MerchantPointOfInterest.create(map)

        ignoreAsserts = []
        
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.pageOffset", response.get("MerchantPOIResponse.pageOffset"),"0")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.totalCount", response.get("MerchantPOIResponse.totalCount"),"2000")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].merchantName", response.get("MerchantPOIResponse.places.place[0].merchantName"),"SABAS WESTERN WEAR")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedMerchantName", response.get("MerchantPOIResponse.places.place[0].cleansedMerchantName"),"SABA'S WESTERN WEAR")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].streetAddr", response.get("MerchantPOIResponse.places.place[0].streetAddr"),"67 W BOSTON")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedStreetAddr", response.get("MerchantPOIResponse.places.place[0].cleansedStreetAddr"),"67 W BOSTON ST")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cityName", response.get("MerchantPOIResponse.places.place[0].cityName"),"CHANDLER")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedCityName", response.get("MerchantPOIResponse.places.place[0].cleansedCityName"),"CHANDLER")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].stateProvidenceCode", response.get("MerchantPOIResponse.places.place[0].stateProvidenceCode"),"AZ")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedStateProvidenceCode", response.get("MerchantPOIResponse.places.place[0].cleansedStateProvidenceCode"),"AZ")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].postalCode", response.get("MerchantPOIResponse.places.place[0].postalCode"),"85225")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedPostalCode", response.get("MerchantPOIResponse.places.place[0].cleansedPostalCode"),"85225-7801")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].countryCode", response.get("MerchantPOIResponse.places.place[0].countryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedCountryCode", response.get("MerchantPOIResponse.places.place[0].cleansedCountryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].telephoneNumber", response.get("MerchantPOIResponse.places.place[0].telephoneNumber"),"4809634496")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedTelephoneNumber", response.get("MerchantPOIResponse.places.place[0].cleansedTelephoneNumber"),"(480) 963-4496")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].mccCode", response.get("MerchantPOIResponse.places.place[0].mccCode"),"5999")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].legalCorporateName", response.get("MerchantPOIResponse.places.place[0].legalCorporateName"),"SABA'S WESTERN WEAR")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cleansedLegalCorporateName", response.get("MerchantPOIResponse.places.place[0].cleansedLegalCorporateName"),"DAVID'S WESTERN STORES  INC.")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].industry", response.get("MerchantPOIResponse.places.place[0].industry"),"DVG")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].superIndustry", response.get("MerchantPOIResponse.places.place[0].superIndustry"),"GEN")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].dateEstablished", response.get("MerchantPOIResponse.places.place[0].dateEstablished"),"12/31/1997")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].newBusinessFlag", response.get("MerchantPOIResponse.places.place[0].newBusinessFlag"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].inBusiness7DayFlag", response.get("MerchantPOIResponse.places.place[0].inBusiness7DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].inBusiness30DayFlag", response.get("MerchantPOIResponse.places.place[0].inBusiness30DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].inBusiness60DayFlag", response.get("MerchantPOIResponse.places.place[0].inBusiness60DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].inBusiness90DayFlag", response.get("MerchantPOIResponse.places.place[0].inBusiness90DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].inBusiness180DayFlag", response.get("MerchantPOIResponse.places.place[0].inBusiness180DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].inBusiness360DayFlag", response.get("MerchantPOIResponse.places.place[0].inBusiness360DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].latitude", response.get("MerchantPOIResponse.places.place[0].latitude"),"33.302154")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].longitude", response.get("MerchantPOIResponse.places.place[0].longitude"),"-111.842276")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].geocodeQualityIndicator", response.get("MerchantPOIResponse.places.place[0].geocodeQualityIndicator"),"STOREFRONT")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].primaryChannelOfDistribution", response.get("MerchantPOIResponse.places.place[0].primaryChannelOfDistribution"),"B")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].cashBack", response.get("MerchantPOIResponse.places.place[0].cashBack"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].payAtThePump", response.get("MerchantPOIResponse.places.place[0].payAtThePump"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].nfcFlag", response.get("MerchantPOIResponse.places.place[0].nfcFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].aggregateMerchantId", response.get("MerchantPOIResponse.places.place[0].aggregateMerchantId"),"5999")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].aggregateMerchantName", response.get("MerchantPOIResponse.places.place[0].aggregateMerchantName"),"NON-AGGREGATED MISCELLANEOUS AND SPECIALTY RETAIL STORES 5999")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].keyAggregateMerchantId", response.get("MerchantPOIResponse.places.place[0].keyAggregateMerchantId"),"5999")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].parentAggregateMerchantId", response.get("MerchantPOIResponse.places.place[0].parentAggregateMerchantId"),"10001460")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].parentAggregateMerchantName", response.get("MerchantPOIResponse.places.place[0].parentAggregateMerchantName"),"NON-AGGREGATED")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].msaCode", response.get("MerchantPOIResponse.places.place[0].msaCode"),"6200")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].naicsCode", response.get("MerchantPOIResponse.places.place[0].naicsCode"),"453998")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].dmaCode", response.get("MerchantPOIResponse.places.place[0].dmaCode"),"753")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[0].locationId", response.get("MerchantPOIResponse.places.place[0].locationId"),"55476524")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].merchantName", response.get("MerchantPOIResponse.places.place[1].merchantName"),"THAKU'S MENS WEAR")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedMerchantName", response.get("MerchantPOIResponse.places.place[1].cleansedMerchantName"),"THAKU'S MENS WEAR")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].streetAddr", response.get("MerchantPOIResponse.places.place[1].streetAddr"),"4320 N SCOTTSDALE ROAD")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedStreetAddr", response.get("MerchantPOIResponse.places.place[1].cleansedStreetAddr"),"4320 N SCOTTSDALE RD")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cityName", response.get("MerchantPOIResponse.places.place[1].cityName"),"SCOTTSDALE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedCityName", response.get("MerchantPOIResponse.places.place[1].cleansedCityName"),"SCOTTSDALE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].stateProvidenceCode", response.get("MerchantPOIResponse.places.place[1].stateProvidenceCode"),"AZ")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedStateProvidenceCode", response.get("MerchantPOIResponse.places.place[1].cleansedStateProvidenceCode"),"AZ")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].postalCode", response.get("MerchantPOIResponse.places.place[1].postalCode"),"85251")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedPostalCode", response.get("MerchantPOIResponse.places.place[1].cleansedPostalCode"),"85251-3312")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].countryCode", response.get("MerchantPOIResponse.places.place[1].countryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedCountryCode", response.get("MerchantPOIResponse.places.place[1].cleansedCountryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].telephoneNumber", response.get("MerchantPOIResponse.places.place[1].telephoneNumber"),"4809477070")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedTelephoneNumber", response.get("MerchantPOIResponse.places.place[1].cleansedTelephoneNumber"),"(480) 947-7070")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].mccCode", response.get("MerchantPOIResponse.places.place[1].mccCode"),"5611")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].legalCorporateName", response.get("MerchantPOIResponse.places.place[1].legalCorporateName"),"THAKU'S MENSWEAR")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cleansedLegalCorporateName", response.get("MerchantPOIResponse.places.place[1].cleansedLegalCorporateName"),"THAKU OF HONG KONG  INC.")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].industry", response.get("MerchantPOIResponse.places.place[1].industry"),"AAM")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].superIndustry", response.get("MerchantPOIResponse.places.place[1].superIndustry"),"AAP")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].dateEstablished", response.get("MerchantPOIResponse.places.place[1].dateEstablished"),"12/31/1997")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].newBusinessFlag", response.get("MerchantPOIResponse.places.place[1].newBusinessFlag"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].inBusiness7DayFlag", response.get("MerchantPOIResponse.places.place[1].inBusiness7DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].inBusiness30DayFlag", response.get("MerchantPOIResponse.places.place[1].inBusiness30DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].inBusiness60DayFlag", response.get("MerchantPOIResponse.places.place[1].inBusiness60DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].inBusiness90DayFlag", response.get("MerchantPOIResponse.places.place[1].inBusiness90DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].inBusiness180DayFlag", response.get("MerchantPOIResponse.places.place[1].inBusiness180DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].inBusiness360DayFlag", response.get("MerchantPOIResponse.places.place[1].inBusiness360DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].latitude", response.get("MerchantPOIResponse.places.place[1].latitude"),"33.499019")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].longitude", response.get("MerchantPOIResponse.places.place[1].longitude"),"-111.926223")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].geocodeQualityIndicator", response.get("MerchantPOIResponse.places.place[1].geocodeQualityIndicator"),"STOREFRONT")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].primaryChannelOfDistribution", response.get("MerchantPOIResponse.places.place[1].primaryChannelOfDistribution"),"B")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].cashBack", response.get("MerchantPOIResponse.places.place[1].cashBack"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].payAtThePump", response.get("MerchantPOIResponse.places.place[1].payAtThePump"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].nfcFlag", response.get("MerchantPOIResponse.places.place[1].nfcFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].aggregateMerchantId", response.get("MerchantPOIResponse.places.place[1].aggregateMerchantId"),"5611")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].aggregateMerchantName", response.get("MerchantPOIResponse.places.place[1].aggregateMerchantName"),"NON-AGGREGATED MEN'S AND BOY'S CLOTHING AND ACCESSORIES STOR 5611")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].keyAggregateMerchantId", response.get("MerchantPOIResponse.places.place[1].keyAggregateMerchantId"),"5611")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].parentAggregateMerchantId", response.get("MerchantPOIResponse.places.place[1].parentAggregateMerchantId"),"10001460")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].parentAggregateMerchantName", response.get("MerchantPOIResponse.places.place[1].parentAggregateMerchantName"),"NON-AGGREGATED")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].msaCode", response.get("MerchantPOIResponse.places.place[1].msaCode"),"6200")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].naicsCode", response.get("MerchantPOIResponse.places.place[1].naicsCode"),"424320")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].dmaCode", response.get("MerchantPOIResponse.places.place[1].dmaCode"),"753")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[1].locationId", response.get("MerchantPOIResponse.places.place[1].locationId"),"55475954")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].merchantName", response.get("MerchantPOIResponse.places.place[2].merchantName"),"VAN HEUSEN #071")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedMerchantName", response.get("MerchantPOIResponse.places.place[2].cleansedMerchantName"),"VAN HEUSEN")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].streetAddr", response.get("MerchantPOIResponse.places.place[2].streetAddr"),"COOGAN BLVD")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedStreetAddr", response.get("MerchantPOIResponse.places.place[2].cleansedStreetAddr"),"1 COOGAN BLVD")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cityName", response.get("MerchantPOIResponse.places.place[2].cityName"),"MYSTIC")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedCityName", response.get("MerchantPOIResponse.places.place[2].cleansedCityName"),"MYSTIC")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].stateProvidenceCode", response.get("MerchantPOIResponse.places.place[2].stateProvidenceCode"),"CT")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedStateProvidenceCode", response.get("MerchantPOIResponse.places.place[2].cleansedStateProvidenceCode"),"CT")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].postalCode", response.get("MerchantPOIResponse.places.place[2].postalCode"),"06355")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedPostalCode", response.get("MerchantPOIResponse.places.place[2].cleansedPostalCode"),"06355-1927")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].countryCode", response.get("MerchantPOIResponse.places.place[2].countryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedCountryCode", response.get("MerchantPOIResponse.places.place[2].cleansedCountryCode"),"USA")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].telephoneNumber", response.get("MerchantPOIResponse.places.place[2].telephoneNumber"),"8605729972")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedTelephoneNumber", response.get("MerchantPOIResponse.places.place[2].cleansedTelephoneNumber"),"8605729972")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].mccCode", response.get("MerchantPOIResponse.places.place[2].mccCode"),"5611")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].legalCorporateName", response.get("MerchantPOIResponse.places.place[2].legalCorporateName"),"VAN HEUSEN RETAI")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cleansedLegalCorporateName", response.get("MerchantPOIResponse.places.place[2].cleansedLegalCorporateName"),"VAN HEUSEN RETAI")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].industry", response.get("MerchantPOIResponse.places.place[2].industry"),"AAF")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].superIndustry", response.get("MerchantPOIResponse.places.place[2].superIndustry"),"AAP")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].dateEstablished", response.get("MerchantPOIResponse.places.place[2].dateEstablished"),"12/31/1997")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].newBusinessFlag", response.get("MerchantPOIResponse.places.place[2].newBusinessFlag"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].inBusiness7DayFlag", response.get("MerchantPOIResponse.places.place[2].inBusiness7DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].inBusiness30DayFlag", response.get("MerchantPOIResponse.places.place[2].inBusiness30DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].inBusiness60DayFlag", response.get("MerchantPOIResponse.places.place[2].inBusiness60DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].inBusiness90DayFlag", response.get("MerchantPOIResponse.places.place[2].inBusiness90DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].inBusiness180DayFlag", response.get("MerchantPOIResponse.places.place[2].inBusiness180DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].inBusiness360DayFlag", response.get("MerchantPOIResponse.places.place[2].inBusiness360DayFlag"),"TRUE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].latitude", response.get("MerchantPOIResponse.places.place[2].latitude"),"41.372157")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].longitude", response.get("MerchantPOIResponse.places.place[2].longitude"),"-71.955404")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].geocodeQualityIndicator", response.get("MerchantPOIResponse.places.place[2].geocodeQualityIndicator"),"STOREFRONT")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].primaryChannelOfDistribution", response.get("MerchantPOIResponse.places.place[2].primaryChannelOfDistribution"),"B")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].cashBack", response.get("MerchantPOIResponse.places.place[2].cashBack"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].payAtThePump", response.get("MerchantPOIResponse.places.place[2].payAtThePump"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].nfcFlag", response.get("MerchantPOIResponse.places.place[2].nfcFlag"),"FALSE")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].aggregateMerchantId", response.get("MerchantPOIResponse.places.place[2].aggregateMerchantId"),"11917")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].aggregateMerchantName", response.get("MerchantPOIResponse.places.place[2].aggregateMerchantName"),"VAN HEUSEN")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].keyAggregateMerchantId", response.get("MerchantPOIResponse.places.place[2].keyAggregateMerchantId"),"11917")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].parentAggregateMerchantId", response.get("MerchantPOIResponse.places.place[2].parentAggregateMerchantId"),"10000205")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].parentAggregateMerchantName", response.get("MerchantPOIResponse.places.place[2].parentAggregateMerchantName"),"PHILLIPS-VAN HEUSEN CORP")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].naicsCode", response.get("MerchantPOIResponse.places.place[2].naicsCode"),"448140")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].dmaCode", response.get("MerchantPOIResponse.places.place[2].dmaCode"),"533")
        self.customAssertEqual(ignoreAsserts, "MerchantPOIResponse.places.place[2].locationId", response.get("MerchantPOIResponse.places.place[2].locationId"),"55475387")
        

        BaseTest.putResponse("example_merchantpoi", response)
        

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

