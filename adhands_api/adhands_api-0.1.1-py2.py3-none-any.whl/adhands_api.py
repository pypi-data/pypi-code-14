# -*- coding: utf-8 -*-
from urllib.parse import urlencode

import requests


class AdhandsException(Exception):
    pass


class AdhandsInternalError(Exception):
    pass


class AdhandsApi:
    def __init__(self, api_url='http://api.adhands.ru', app_id=None, user_id=None, login=None, password=None):
        self.url = api_url
        self.app_id = app_id
        self.user_id = user_id
        self.login = login
        self.password = password
        self.token = None

    def get_token(self):
        if not self.token:
            params = {
                'login': self.login,
                'userId': self.user_id,
                'applicationId': self.app_id,
                'grantType': 'password',
                'password': self.password
            }

            params = {k: v for k, v in params.items() if v}
            response = requests.post('{}/getToken'.format(self.url), urlencode(params))
            self.check_response(response)
            self.token = response.json()['token']

        return self.token

    def make_request(self, method=None, data=None):
        token = self.get_token()
        params = {
            'method': method,
            'userId': self.user_id,
            'login': self.login,
            'applicationId': self.app_id,
            'token': token,
            'args': data
        }
        response = requests.post('{}/v1'.format(self.url), json=params)
        self.check_response(response)

        return response.json()

    @staticmethod
    def check_response(response):
        if response.status_code != requests.codes.ok:
            raise AdhandsInternalError()
        r = response.json()
        if 'code' in r:
            if 400 <= r['code'] <= 503:
                raise AdhandsException('#{}: {}'.format(r['code'], r['detail']))
        elif 'error' in r:
            raise AdhandsException(r['error'])

