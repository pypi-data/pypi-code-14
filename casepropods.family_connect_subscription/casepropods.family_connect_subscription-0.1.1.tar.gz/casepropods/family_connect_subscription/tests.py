import json
import responses
from django.apps import apps
from casepro.cases.models import Case
from casepro.test import BaseCasesTest
from .plugin import SubscriptionPodConfig, SubscriptionPod


class SubscriptionPodTest(BaseCasesTest):
    def setUp(self):
        super(SubscriptionPodTest, self).setUp()
        self.contact = self.create_contact(self.unicef, 'test_id', "Tester")
        self.msg1 = self.create_message(
            self.unicef, 123, self.contact, "Test message")
        self.case = Case.get_or_open(
            self.unicef, self.user1, self.msg1, "Summary", self.moh)
        self.base_url = 'http://example.com/'

        self.pod = SubscriptionPod(
            apps.get_app_config('family_connect_subscription_pod'),
            SubscriptionPodConfig({
                'index': 23,
                'title': "My subscription Pod",
                'url': "http://example.com/",
                'token': "test_token",
            }))

    def subscription_callback_no_matches(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
        return (200, headers, json.dumps(resp))

    def subscription_callback_one_match(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
                "url": "http://example.com/api/v1/subscriptions/sub_id/",
                "id": "sub_id",
                "version": 1,
                "identity": "C-002",
                "messageset": 1,
                "next_sequence_number": 1,
                "lang": "eng",
                "active": True,
                "completed": False,
                "schedule": 1,
                "process_status": 0,
                "metadata": None,
                "created_at": "2016-07-22T15:53:42.282902Z",
                "updated_at": "2016-09-06T17:17:54.746390Z"
            }]
        }
        return (200, headers, json.dumps(resp))

    def message_set_callback(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "id": 1,
            "short_name": "test_set",
            "content_type": "text",
            "notes": "",
            "next_set": None,
            "default_schedule": 1,
            "created_at": "2016-07-22T15:52:16.308779Z",
            "updated_at": "2016-07-22T15:52:16.308802Z"
        }
        return (200, headers, json.dumps(resp))

    def schedule_callback(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "id": 1,
            "minute": "0",
            "hour": "8",
            "day_of_week": "1,2",
            "day_of_month": "*",
            "month_of_year": "*"
        }
        return (200, headers, json.dumps(resp))

    def error_callback(self, request):
        headers = {'Content-Type': "application/json"}
        resp = {
            "detail": "Bad Request"
        }
        return (400, headers, json.dumps(resp))

    @responses.activate
    def test_read_data_no_subscriptions(self):
        # Add callback
        responses.add_callback(
            responses.GET,
            self.base_url + 'subscriptions/?identity=' + self.contact.uuid,
            callback=self.subscription_callback_no_matches,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        auth_header = responses.calls[0].request.headers['Authorization']
        self.assertEqual(auth_header, "Token test_token")
        self.assertEqual(result, {"items": [{
            "rows": [{
                "name": "No subscriptions", "value": ""
            }]}]})

    @responses.activate
    def test_read_data_one_subscription(self):
        # Add callbacks
        responses.add_callback(
            responses.GET,
            self.base_url + 'subscriptions/?identity=' + self.contact.uuid,
            callback=self.subscription_callback_one_match,
            match_querystring=True, content_type="application/json")
        responses.add_callback(
            responses.GET, self.base_url + 'messageset/1/',
            callback=self.message_set_callback,
            match_querystring=True, content_type="application/json")
        responses.add_callback(
            responses.GET, self.base_url + 'schedule/1/',
            callback=self.schedule_callback,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        auth_header = responses.calls[0].request.headers['Authorization']
        self.assertEqual(auth_header, "Token test_token")
        self.assertEqual(result, {"items": [
            {"rows": [
                {"name": "Message Set", "value": "test_set"},
                {"name": "Next Sequence Number", "value": 1},
                {"name": "Schedule",
                 "value": "At 08:00 every Monday and Tuesday"},
                {"name": "Active", "value": True},
                {"name": "Completed", "value": False},
            ]}
        ]})

    @responses.activate
    def test_read_data_error_case(self):
        # Add callback
        responses.add_callback(
            responses.GET,
            self.base_url + 'subscriptions/?identity=' + self.contact.uuid,
            callback=self.error_callback,
            match_querystring=True, content_type="application/json")

        result = self.pod.read_data({'case_id': self.case.id})

        auth_header = responses.calls[0].request.headers['Authorization']
        self.assertEqual(auth_header, "Token test_token")
        self.assertEqual(result, {"items": [
            {"name": "Error", "value": "Bad Request"}
        ]})
