import json
import httplib

from . import token
from errors import (
    AuthenticationError
)


class APIKey:
    '''
    represents an API key to be used for authentication
    '''
    def __init__(self, secret="", client=""):
        '''
        initializes a new instance of the APIKey class

        Args:
          secret (str): the secret string of this APIKey
          client (str): the client name for this APIKey
        '''
        self.client = client
        self.secret = secret

    def auth(self, client):
        '''
        authenticates the given client using this auth method

        Args:
            client (ktrlpy.Client): the client to authenticate
        Returns:
            an error object if failed
        '''
        msg = {
            "Client": self.client,
            "Secret": self.secret
        }

        # TODO routes should be configured
        url = client.get_request_url("/session/create/token")

        client.request(
            "POST",
            url,
            json.dumps(msg),
            {"Content-Type": "application/json"}
        )

        resp = client.getresponse()

        return handle_auth_response(resp, client)


class UserInfo:
    '''
    represents a uername and password pair to be used
    for authentication
    '''
    def __init__(self, username="", password=""):
        '''
        initializes a new instance of UserInfo

        Args:
          username (str): the username of this user
          password (str): the password for this username
        '''
        self.username = username
        self.password = password

    def auth(self, client):
        '''
        authenticates the given client using this auth method

        Args:
            client (ktrlpy.Client): the client to authenticate
        Returns:
            an error object if failed
        '''
        msg = {
            "username": self.username,
            "password": self.password
        }

        # TODO routes should be configured
        url = client.get_request_url("/session/create/user")

        client.request(
            "POST",
            url,
            json.dumps(msg),
            {"Content-Type": "application/json"}
        )

        resp = client.getresponse()

        return handle_auth_response(resp, client)


def handle_auth_response(resp, client):
    '''
    handles a response from the ktrlio servers
    after an authentication attempt

    Args:
        resp (httplib.Response): the response to the auth request
        client (ktrlpy.Client): the client this auth request was for
    Returns:
        an error if something wasn't right
    '''
    client.token_data = None
    client.token_raw = ""

    body = resp.read()

    if resp.status == httplib.OK:
        # expect a json web token on success
        t = token.ParseClaims(body, validate=(not client.insecure_skip_verify))
        if t is None:
            return ValueError("server returned invalid json web token")
        client.token_data = t
        client.token_raw = body
        return None

    elif resp.status == httplib.UNAUTHORIZED:
        return AuthenticationError(
            "authentication failed for {}".format(client.base_url))

    return RuntimeError(
        "unhandled auth reaponse status {}".format(resp.status))
