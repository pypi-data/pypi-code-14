import endpoints
import json
from protorpc import message_types
from protorpc import messages
from protorpc import remote
import unittest
import webtest


class Echo(messages.Message):
    """A proto Message that contains a simple string field."""
    content = messages.StringField(1)
# [END messages]

ECHO_CONTAINER = endpoints.ResourceContainer(
    message_types.VoidMessage,
    msg=messages.StringField(1)
)


# [START echo_api]
@endpoints.api(name='echo', version='v1')
class EchoApi(remote.Service):

    @endpoints.method(
        # This method takes an Echo message.
        Echo,
        # This method returns an Echo message.
        Echo,
        path='echo',
        http_method='POST',
        name='echo')
    def echo(self, request):
        return Echo(content=request.content)

    @endpoints.method(
        ECHO_CONTAINER,
        Echo,
        path='path/{msg}',
        http_method='GET',
        name='path'
    )
    def path(self, request):
        return Echo(content=request.msg)

    @endpoints.method(
        ECHO_CONTAINER,
        Echo,
        path='query',
        http_method='GET',
        name='query'
    )
    def query(self, request):
        return Echo(content=request.msg)
# [END echo_api]


# [START api_server]
api = endpoints.api_server([EchoApi])
# [END api_server]


BODY = {'content': 'test test'}


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(api)

    def testEcho(self):
        resp = self.app.post_json('/_ah/api/echo/v1/echo', BODY)
        self.assertEqual(BODY, resp.json)

    def testPath(self):
        resp = self.app.get('/_ah/api/echo/v1/path/test+test')
        self.assertEqual(BODY, resp.json)

    def testQuery(self):
        resp = self.app.get('/_ah/api/echo/v1/query?msg=test+test')
        self.assertEqual(BODY, resp.json)

if __name__ == '__main__':
    unittest.main()
