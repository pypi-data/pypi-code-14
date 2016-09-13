from applause import __program_name__, __version__
import logging

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests
from applause.errors import InvalidLogin


from . import settings


class ApplauseAuth(object):
    """
    Handles Applause's 3 legged OAuth API.
    """

    def __init__(self, client_id, client_secret, oauth_base_url=None):
        self.client_id = client_id
        self.client_secret = client_secret

        self.session = requests.Session()
        self.session.auth = (client_id, client_secret)

        self.access_token = None

        self.oauth_base_url = oauth_base_url or settings.OAUTH_BASE_URL

    @staticmethod
    def get_oauth_token_url(oauth_base_url):
        return urljoin(oauth_base_url, "/auth/token")

    @staticmethod
    def generate_requests_session(access_token):
        """
        Generates a new requests `Session` object objects with all the
        necessary auth headers and version header for debug purposes set.
        """
        session = requests.Session()
        session.headers = {
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
            "User-Agent": "%s v.%s" % (__program_name__, __version__)
        }

        return session

    def _get_access_token(self, username, password):
        """
        Gets an access token from the auth-service using the
        Resource Owner Client Credentials Grant Flow (OAuth2).
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'rememberMe': 'on'
        }

        url = self.get_oauth_token_url(self.oauth_base_url)
        response = self.session.post(url, data=data, headers=headers)

        if not response.ok:
            logging.debug("Response: {data}".format(data=response.content))
            raise InvalidLogin("Could not get a new access token. Please check your credentials.")

        data = response.json().get('data', None)
        return data.get('access_token', None) if data else None

    def login(self, username=None, password=None, access_token=None):
        """
        Initiates user session with one of the following arguments:
        * username, password
        """
        if username and password:
            logging.debug("Logging in with username & password")
            self.access_token = self._get_access_token(username, password)
        else:
            logging.debug("Logging in with access token")
            self.access_token = access_token

        if not self.access_token:
            raise InvalidLogin("Could not use an existing or fetch a new access token. Please try again.")

        return self.generate_requests_session(self.access_token)

    def logged_in(self):
        """
        Returns true if a user auth session has been initiated.
        """
        return self.access_token is not None
