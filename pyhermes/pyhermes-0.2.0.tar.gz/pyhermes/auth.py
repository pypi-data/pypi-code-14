import abc

import requests
import six


class AuthenticationError(Exception):
    pass


class HermesAuthorization(object, six.with_metaclass(abc.ABCMeta)):
    @abc.abstractmethod
    def get_auth_headers(self):
        raise NotImplementedError()


class OAuth2Client(HermesAuthorization):
    def __init__(
        self, url, client_id, secret, username, password,
    ):
        self.client_id = client_id
        self.secret = secret
        self.username = username
        self.password = password
        self.url = url
        self._token = None

    @property
    def token(self):
        if not self._token:
            self._token = self._get_token()
        return self._token

    def _get_token(self):
        data = 'grant_type=password&username={}&password={}'.format(
            self.username, self.password
        )
        response = requests.post(
            self.url, auth=(self.client_id, self.secret), data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        if response.status_code != 200:
            raise AuthenticationError('OAuth authentication failed')
        return response.json()['access_token']

    def get_auth_headers(self):
        return {"Authorization": "Token " + self.token}
