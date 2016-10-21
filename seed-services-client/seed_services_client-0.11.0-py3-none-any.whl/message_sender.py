from demands import JSONServiceClient, HTTPServiceClient


class MessageSenderApiClient(object):
    """
    Client for Message Sender Service.

    :param str auth_token:

        An access token.

    :param str api_url:
        The full URL of the API.

    """

    def __init__(self, auth_token, api_url, session=None, session_http=None):
        if session is None:
            session = JSONServiceClient(
                url=api_url, headers={'Authorization': 'Token ' + auth_token})

        if session_http is None:
            session_http = HTTPServiceClient(
                url=api_url, headers={'Authorization': 'Token ' + auth_token})
        self.session = session
        self.session_http = session_http

    def create_outbound(self, payload):
        return self.session.post('/outbound/', data=payload)
