"""OAuth2  handlers and some utility functions for RingPlus."""

from __future__ import print_function

import requests
from requests_oauthlib import OAuth2, OAuth2Session

from bs4 import BeautifulSoup


class OAuthHandler(object):
    """OAuth Authentication Handler.

    OAuthHandler is used to simplify the OAuth2 authentication process.

    All authentication into the RingPlus API must been done using OAuth 2.0
    over HTTPS. It allows applications to access user details without needing
    their password, allows limiting access to only what the application
    requires, and can be revoked by users at any time.

    All application developers need to register their application by visiting
    the Application tab on their Settings page. A registered application is
    assigned a Client ID and Client Secret. Your Client Secret should not be
    shared with anyone.

    Using your Client ID and Secret, you will be able to get an Authorization
    Token for a user, and make requests to the API for their data.
    """

    AUTHORIZATION_BASE_URL = 'https://my.ringplus.net/oauth/authorize'
    TOKEN_URL = 'https://my.ringplus.net/oauth/token'

    def __init__(self, client_id, client_secret, redirect_uri):
        """OAuthHandler instance contructor.

        Args:
            client_id: Client ID associated with the app.
            client_secret: Client secret.
            redirect_uri: The redirect URI exactly as listed on RingPlus.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)

    def get_authorization_url(self, **kwargs):
        """Returns the authorization URL to redirect users."""
        response = self.oauth.authorization_url(self.AUTHORIZATION_BASE_URL,
                                                **kwargs)
        authorization_url, state = response
        return authorization_url

    def fetch_token(self, authorization_response):
        """Use the authorization response url to fetch a token.

        Returns:
            dict: A dictionary representing the token.
        """
        token = self.oauth.fetch_token(
            self.TOKEN_URL,
            authorization_response=authorization_response,
            client_secret=self.client_secret)
        return token

    def refresh_token(self):
        """Refresh the current access token."""
        data = {'grant_type': 'refresh_token',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': self.access_token['refresh_token']}
        post = requests.post(self.TOKEN_URL, data=data)
        self.access_token = post.json()

    def login(self, username, password, **kwargs):
        """Hackish method to sign into RingPlus without going to site.

        This sets the access token for the OAutherHandler instance.

        Args:
            username: Username used to login to Ring Plus (likely your email).
            password: The password used to login to Ring Plus.
        """
        session = requests.Session()
        params = {'response_type': 'code',
                  'client_id': self.client_id,
                  'redirect_uri': self.redirect_uri}
        # Go to authorization url and get the necessary details
        r1 = session.get(self.get_authorization_url(**kwargs), params=params)
        data = self._get_input_data_from_html(r1.content)
        self._set_username_and_password(data, username, password)

        # Login with username and password
        r2 = session.post(r1.url, data=data)
        r2.raise_for_status()

        self.access_token = self.fetch_token(r2.url)

    def get_account_id(self):
        """Return the account id associated with the access token."""
        raise NotImplementedError

    def get_user_id(self):
        """Return the first user id associated with the access token."""
        raise NotImplementedError

    def apply_auth(self):
        return OAuth2(self.client_id, token=self.access_token)

    def _get_input_data_from_html(self, html):
        """Return the params needed to login from html."""
        soup = BeautifulSoup(html, 'html.parser')
        input_tags = soup.find_all('input')

        # Get the data from the tags
        data = {}
        for tag in input_tags:
            data[tag.attrs['name']] = tag.attrs.get('value', None)
        return data

    def _set_username_and_password(self, data, username, password):
        """Adds username and password to input dictionary."""
        for key in data.keys():
            if 'email' in key:
                data[key] = username
            if 'password' in key:
                data[key] = password
