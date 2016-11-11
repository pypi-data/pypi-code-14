# -*- coding: utf-8 -*-

"""
F5 BIG-IQ auth plugin for HTTPie.
"""
import requests
import urlparse
import jwt
from datetime import datetime
from httpie.plugins import AuthPlugin

__version__ = '0.0.2'
__author__ = 'ivan mecimore'
__license__ = 'MIT'


def make_url(r, path):
    url = urlparse.urlsplit(r.url)
    url = url._replace(path=path)
    return urlparse.urlunsplit(url)


class XF5AuthToken(object):

    def __init__(self, token):
        self.token = token

    def is_expired(self):
        decoded = jwt.decode(self.token, verify=False)
        return datetime.utcfromtimestamp(decoded.get('exp', 0)) <= datetime.utcnow()

    def get_token(self):
        return self.token


class F5Auth(object):
    """XF5Auth to set the right X-F5-Auth-Token header"""

    _login_path = '/mgmt/shared/authn/login'
    _exchange_path = '/mgmt/shared/authn/exchange'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def __call__(self, r):
        if not self.access_token and not self.refresh_token:
            self.get_new_tokens(r)

        # since we aren't caching tokens now this should never happen
        if self.access_token.is_expired():
            self.refresh_token(r)

        r.headers['X-F5-Auth-Token'] = self.access_token.get_token()
        return r

    def get_new_tokens(self, r):
        url = make_url(r, self._login_path)
        resp = requests.post(url, json={'username': self.username, 'password': self.password}, verify=False)
        resp_json = resp.json()
        self.access_token = XF5AuthToken(resp_json['token']['token'])
        self.refresh_token = XF5AuthToken(resp_json['refreshToken']['token'])

    def exchange_token(self, r):
        if self.refresh_token.is_expired():
            raise Exception('Exchange token is expired.')

        url = make_url(r, self._exchange_path)
        resp = requests.post(url, data={'refreshToken': self.refresh_token}, verify=False)
        self.access_token = resp.json()['token']


class F5AuthPlugin(AuthPlugin):
    """Plugin registration"""

    name = 'X-F5-Auth-Token auth'
    auth_type = 'xf5'
    description = 'Authenticate using an X-F5-Auth-Token'

    def get_auth(self, username, password):
        return F5Auth(username, password)
