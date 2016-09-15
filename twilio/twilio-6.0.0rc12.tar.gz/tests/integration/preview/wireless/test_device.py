# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio.exceptions import TwilioException
from twilio.http.response import Response


class DeviceTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.preview.wireless.devices(sid="DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://preview.twilio.com/wireless/Devices/DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.preview.wireless.devices.list()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://preview.twilio.com/wireless/Devices',
        ))

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.preview.wireless.devices.create(rate_plan="rate_plan")
        
        values = {
            'RatePlan': "rate_plan",
        }
        
        self.holodeck.assert_has_request(Request(
            'post',
            'https://preview.twilio.com/wireless/Devices',
            data=values,
        ))

    def test_update_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.preview.wireless.devices(sid="DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").update()
        
        self.holodeck.assert_has_request(Request(
            'post',
            'https://preview.twilio.com/wireless/Devices/DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))
