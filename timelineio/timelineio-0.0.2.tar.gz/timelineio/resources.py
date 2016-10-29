# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import sys

import requests

from timelineio import __version__
from timelineio.exceptions import TimelineIOAPIError


class TimelineIOBaseResource(object):
    endpoint = ''  # Must be set on children classes.

    def __init__(self, base_api_url, auth_credentials, auth_token):
        self.base_api_url = base_api_url
        self.auth_credentials = auth_credentials
        self.auth_token = auth_token

    def get_full_endpoint(self, path):
        return '{}{}'.format(self.base_api_url, path)

    def get_full_list_endpoint(self):
        return self.get_full_endpoint(self.endpoint)

    def get_full_details_endpoint(self, identifier):
        return '{}/{}'.format(self.get_full_list_endpoint(), identifier)

    def _request(self, requests_method, url, data=None, params=None):
        auth = None
        headers = {
            'user-agent': 'timelineio/{} python/{}'.format(__version__, sys.version.split()[0]),
        }

        if self.auth_token:
            headers['Authorization'] = 'Token {}'.format(self.auth_token)
        elif self.auth_credentials:
            auth = self.auth_credentials

        try:
            return requests_method(url, auth=auth, headers=headers, data=data, params=params)
        except requests.exceptions.RequestException as e:
            raise TimelineIOAPIError('{}'.format(e))

    def list(self, limit=30, offset=0):
        return self._request(requests.get, self.get_full_list_endpoint(), params={'limit': limit, 'offset': offset})

    def create(self, **data):
        return self._request(requests.post, self.get_full_list_endpoint(), data=data)

    def retrieve(self, identifier):
        return self._request(requests.get, self.get_full_details_endpoint(identifier))

    def update(self, identifier, **data):
        return self._request(requests.patch, self.get_full_details_endpoint(identifier), data=data)

    def delete(self, identifier):
        return self._request(requests.delete, self.get_full_details_endpoint(identifier))


class TimelineIOEventResource(TimelineIOBaseResource):
    endpoint = '/api/events'


class TimelineIOCustomerResource(TimelineIOBaseResource):
    endpoint = '/api/customers'

    def list(self, limit=30, offset=0):
        raise RuntimeError('Not allowed')

    def login(self, email, password):
        data = {
            'username': email,
            'password': password,
        }
        return self._request(requests.post, self.get_full_endpoint('/api/auth/login'), data=data)
