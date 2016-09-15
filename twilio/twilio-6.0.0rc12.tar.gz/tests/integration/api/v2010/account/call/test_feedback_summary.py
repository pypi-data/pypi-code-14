# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from datetime import date
from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio import serialize
from twilio.exceptions import TwilioException
from twilio.http.response import Response


class FeedbackSummaryTestCase(IntegrationTestCase):

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .calls \
                                 .feedback_summaries.create(start_date=date(2008, 1, 2), end_date=date(2008, 1, 2))
        
        values = {
            'StartDate': serialize.iso8601_date(date(2008, 1, 2)),
            'EndDate': serialize.iso8601_date(date(2008, 1, 2)),
        }
        
        self.holodeck.assert_has_request(Request(
            'post',
            'https://api.twilio.com/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Calls/FeedbackSummary.json',
            data=values,
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "call_count": 10200,
                "call_feedback_count": 729,
                "end_date": "2011-01-01",
                "include_subaccounts": false,
                "issues": [
                    {
                        "count": 45,
                        "description": "imperfect-audio",
                        "percentage_of_total_calls": "0.04%"
                    }
                ],
                "quality_score_average": 4.5,
                "quality_score_median": 4,
                "quality_score_standard_deviation": 1,
                "sid": "FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "start_date": "2011-01-01",
                "status": "completed",
                "date_created": "Tue, 31 Aug 2010 20:36:28 +0000",
                "date_updated": "Tue, 31 Aug 2010 20:36:44 +0000"
            }
            '''
        ))
        
        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .calls \
                                      .feedback_summaries.create(start_date=date(2008, 1, 2), end_date=date(2008, 1, 2))
        
        self.assertIsNotNone(actual)

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .calls \
                                 .feedback_summaries(sid="FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://api.twilio.com/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Calls/FeedbackSummary/FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "call_count": 10200,
                "call_feedback_count": 729,
                "end_date": "2011-01-01",
                "include_subaccounts": false,
                "issues": [
                    {
                        "count": 45,
                        "description": "imperfect-audio",
                        "percentage_of_total_calls": "0.04%"
                    }
                ],
                "quality_score_average": 4.5,
                "quality_score_median": 4,
                "quality_score_standard_deviation": 1,
                "sid": "FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "start_date": "2011-01-01",
                "status": "completed",
                "date_created": "Tue, 31 Aug 2010 20:36:28 +0000",
                "date_updated": "Tue, 31 Aug 2010 20:36:44 +0000"
            }
            '''
        ))
        
        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .calls \
                                      .feedback_summaries(sid="FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()
        
        self.assertIsNotNone(actual)

    def test_delete_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .calls \
                                 .feedback_summaries(sid="FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()
        
        self.holodeck.assert_has_request(Request(
            'delete',
            'https://api.twilio.com/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Calls/FeedbackSummary/FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.json',
        ))

    def test_delete_response(self):
        self.holodeck.mock(Response(
            204,
            None,
        ))
        
        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .calls \
                                      .feedback_summaries(sid="FSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()
        
        self.assertTrue(actual)
