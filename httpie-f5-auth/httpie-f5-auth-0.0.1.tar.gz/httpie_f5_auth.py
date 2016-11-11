# -*- coding: utf-8 -*-

"""
F5 BIG-IQ auth plugin for HTTPie.
"""
import requests
import urlparse
import jwt
import datetime
from httpie.plugins import AuthPlugin

__version__ = '0.0.1'
__author__ = 'mecimore'
__license__ = 'MIT'


def make_url(r, path):
    url = urlparse.urlparser(r.url)
    host = urlparse.urlunparse(url[0:2])
    return urlparse.urljoin(host, path)


class XF5AuthToken(object):

    def __init__(self, token):
        self.token = token

    def is_expired(self):
        decoded = jwt.decode(self.token, verify=False)
        return decoded['exp'] <= datetime.utcnow()


class F5Auth(object):
    """XF5Auth to set the right X-F5-Auth-Token header"""

    _login_path = '/mgmt/shared/authn/login'
    _exchange_path = '/mgmt/shared/authn/exchange'

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = None
        self.exchange_token = None

    def __call__(self, r):
        if not self.access_token and not self.exchange_token:
            self.get_new_tokens(r)

        if self.access_token.is_expired():
            self.exchange_tokens(r)

        r.headers['X-F5-Auth-Token'] = self.access_token
        return r

    def get_new_tokens(self, r):
        url = make_url(r, self._login_path)
        resp = requests.post(url, data={'username': self.username, 'password': self.password}, verify=False)
        resp_json = resp.json()
        self.access_token = XF5AuthToken(resp_json['token'])
        self.exchange_token = XF5AuthToken(resp.json['exchangeToken'])

    def exchange_token(self, r):
        if self.exchange_token.is_expired():
            raise Exception('Exchange token is expired.')

        url = make_url(r, self._exchange_path)
        resp = requests.post(url, data={'exchangeToken': self.exchange_token}, verify=False)
        self.access_token = resp.json()['token']


class F5AuthPlugin(AuthPlugin):
    """Plugin registration"""

    name = 'X-F5-Auth-Token auth'
    auth_type = 'xf5'
    description = 'Authenticate using an X-F5-Auth-Token'

    def get_auth(self, username, password):
        return F5Auth(username, password)
