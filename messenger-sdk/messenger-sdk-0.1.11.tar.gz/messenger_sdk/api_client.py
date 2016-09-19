from datetime import datetime, timedelta
import logging

from tornado import escape, gen, httpclient
from urllib import parse


class ApiClient:
    def __init__(self):
        self._http = httpclient.AsyncHTTPClient()

    @gen.coroutine
    def async_request(self, url, parameters=None, http_method='GET', body=None, headers=None):
        self._check_method(http_method=http_method)

        url = self.encode_url(url=url, parameters=parameters)
        headers = self._prepare_request_headers(headers=headers)
        if body:
            body = self._validate_body(body)

        try:
            logging.debug('Requesting: {url}'.format(url=url))
            request = self._create_request(url=url, http_method=http_method, headers=headers, body=body)
            response = yield self._http.fetch(request)
            logging.debug('Success: {url}'.format(url=url))
            if response.body:
                return escape.json_decode(response.body)
        except httpclient.HTTPError as e:
            e.message = 'Unable to complete {url}: {message}'.format(url=url, message=e.message)
            raise e

    def _check_method(self, http_method):
        if not self._is_method_valid(http_method):
            raise ValueError('Unsupported method: {method}'.format(method=http_method))

    def _prepare_request_headers(self, headers):
        default_header = {'Content-Type': 'application/json'}
        headers = self.append_headers(header_to_append=default_header, current_headers=headers)

        return headers

    @staticmethod
    def _create_request(url: str, http_method: str, headers: dict, body: str):
        return httpclient.HTTPRequest(url=url, method=http_method, headers=headers, body=body)

    @staticmethod
    def _is_method_valid(http_method):
        supported_methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH']
        return http_method in supported_methods

    @staticmethod
    def encode_url(url: str, parameters=None):
        if parameters:
            if not isinstance(parameters, dict):
                raise TypeError('Parameters must be instance of dict.')
            url = url.strip()
            url += '?' + parse.urlencode(parameters)

        return url

    @staticmethod
    def _is_json_valid(json):
        is_valid = True
        try:
            escape.json_decode(json)
        except TypeError:
            is_valid = False
        return is_valid

    def _validate_body(self, body):
        if isinstance(body, dict):
            body = escape.json_encode(body)
        elif not self._is_json_valid(body):
            raise TypeError('Invalid json format')
        return body

    @staticmethod
    def _is_headers_type_valid(headers):
        return bool(isinstance(headers, dict))

    @staticmethod
    def append_headers(header_to_append: dict, current_headers=None):
        if current_headers is None:
            current_headers = dict()
        else:
            if not isinstance(current_headers, dict):
                raise TypeError(
                    'Invalid type in function append_headers, expected {expected}, {given} given.'.format(
                        expected=dict.__name__,
                        given=type(current_headers)))
        current_headers.update(header_to_append)

        return current_headers


class OAuthApiClient(ApiClient):
    __access_token = None
    __token_expires_at = None

    def __init__(self,
                 oauth_authorization_url,
                 oauth_client_id,
                 oauth_client_secret,
                 oauth_grant_type,
                 username=None,
                 password=None,
                 renew_token_before_seconds=None,
                 non_expiring_token=None):
        super().__init__()
        self._oauth_authorization_url = oauth_authorization_url
        self._oauth_client_id = oauth_client_id
        self._oauth_client_secret = oauth_client_secret
        self._oauth_grant_type = oauth_grant_type
        self._username = username
        self._password = password
        self._renew_token_before_seconds = renew_token_before_seconds
        self._non_expiring_token = non_expiring_token

    @property
    def _access_token(self):
        return self.__access_token

    @_access_token.setter
    def _access_token(self, value):
        self.__access_token = value

    @property
    def _token_expires_at(self):
        return self.__token_expires_at

    @_token_expires_at.setter
    def _token_expires_at(self, expires_in: int):
        self.__token_expires_at = datetime.now() + timedelta(seconds=expires_in)

    @gen.coroutine
    def oauth_async_request(self, url, parameters=None, http_method='GET', body=None, headers=None):
        access_token = yield self._get_valid_access_token()
        auth_header = {'Authorization': 'Bearer {access_token}'.format(access_token=access_token)}
        headers = self.append_headers(header_to_append=auth_header, current_headers=headers)
        response = yield self.async_request(url=url,
                                            parameters=parameters,
                                            http_method=http_method,
                                            body=body,
                                            headers=headers)
        return response

    @gen.coroutine
    def _get_valid_access_token(self):
        if self._renew_token_before_seconds is None:
            self._renew_token_before_seconds = 300

        if self._non_expiring_token is not None:
            return self._non_expiring_token

        if self._access_token is None:
            yield self._oauth_authorization_request(self._oauth_grant_type)
        elif (self.__token_expires_at - datetime.now()).total_seconds() < int(self._renew_token_before_seconds):
            if 'refresh_token' in self._get_supported_grant_types():
                yield self._oauth_authorization_request('refresh_token')
            else:
                yield self._oauth_authorization_request(self._oauth_grant_type)
        return str(self._access_token)

    @gen.coroutine
    def _oauth_authorization_request(self, grant_type, method='POST'):
        url = self._oauth_authorization_url
        payload = self._get_payload(grant_type)
        response = yield self.async_request(url=url, method=method, body=payload)
        self.__access_token = response.get('access_token')
        self._access_token_expires_at = int(response.get('expires_in'))

    def _get_payload(self, grant_type):
        if not self._is_grant_type_valid(grant_type):
            raise ValueError('Unsupported grant type: {grant_type}'.format(grant_type=grant_type))
        payload = {'client_id': self._oauth_client_id, 'client_secret': self._oauth_client_secret}
        if grant_type == 'password':
            payload.update({'username': self._username, 'password': self._password})
        elif grant_type == 'refresh_token':
            if not self._access_token:
                raise ValueError('Cannot refresh empty token: {access_token}.'.format(access_token=self._access_token))
            payload.update({'refresh_token': self._access_token})
        payload.update({'grant_type': grant_type})
        return payload

    @staticmethod
    def _get_supported_grant_types():
        return ['password', 'client_credentials', 'refresh_token']

    def _is_grant_type_valid(self, grant_type):
        is_valid = False
        supported_grant_types = self._get_supported_grant_types()
        if not isinstance(supported_grant_types, list):
            raise TypeError(
                'Function {function} must return list.'.format(function=self._get_supported_grant_types.__name__))
        if grant_type in supported_grant_types:
            is_valid = True
        return is_valid
