import socket

import mock
import testtools

from abclient.common import http
from abclient.tests.unit import fakes


@mock.patch(
    "karbor.services.protection.clients.abclient.common.http.requests.request")
class HTTPClientTest(testtools.TestCase):
    def setUp(self):
        super(HTTPClientTest, self).setUp()

    def test_http_json_request(self, mock_request):
        mock_request.return_value = fakes.FakeHTTPResponse(
            200, "OK", {'content-type': 'application/json'}, "{}")
        client = http.HTTPClient("https://eisoo.com")
        body = client.json_request("GET", '')
        self.assertEqual({}, body)

    def test_http_json_request_with_resp_code_204(self, mock_request):
        mock_request.return_value = fakes.FakeHTTPResponse(
            204, "OK", {"content-type": "application/json"}, '')

        client = http.HTTPClient("https://eisoo.com")
        body = client.json_request("DELETE", '', data={"code": 123})
        self.assertEqual(None, body)

    def test_http_json_request_with_resp_body_is_None(self, mock_request):
        mock_request.return_value = fakes.FakeHTTPResponse(
            200, "OK", {"content-type": "application/json"}, '')

        client = http.HTTPClient("https://eisoo.com")
        body = client.json_request("GET", '', data={})
        self.assertEqual(None, body)

    def test_http_raw_request_with_resp_is_invalid_json(self, mock_request):
        mock_request.return_value = fakes.FakeHTTPResponse(
            200, "OK", {"content-type": "application/json"}, 'not_json')
        client = http.HTTPClient("https://eisoo.com")
        body = client.json_request("GET", '', data={})
        self.assertEqual("Invalid-JSON", body)
