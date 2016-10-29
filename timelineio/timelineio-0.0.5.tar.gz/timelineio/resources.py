# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import sys

import requests

from timelineio import __version__
from timelineio.exceptions import TimelineIOAPIError


class TimelineIORequestMixin(object):
    def __init__(self, base_api_url, auth_credentials, auth_token):
        self.base_api_url = base_api_url
        self.auth_credentials = auth_credentials
        self.auth_token = auth_token

    def get_full_endpoint(self, path):
        return '{}{}'.format(self.base_api_url, path)

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


class TimelineIOBaseResource(TimelineIORequestMixin):
    endpoint = ''  # Must be set on children classes.

    def get_full_list_endpoint(self):
        return self.get_full_endpoint(self.endpoint)

    def get_full_details_endpoint(self, identifier):
        return '{}/{}'.format(self.get_full_list_endpoint(), identifier)

    def list(self, **params):
        '''
        Fetches a list of resources on API. Use params for endpoint query params (pagination, filtering, ordering, etc)
        Example of params:
        - limit, offset (for pagination - defaults to 30 and 0)
        - object_type, object_id, human_identifier (for filtering)
        - fields, exclude (for reducing API response payload)
        - ordering (for... guess what?)
        '''
        params.setdefault('limit', 30)
        params.setdefault('offset', 0)
        return self._request(requests.get, self.get_full_list_endpoint(), params=params)

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


class TimelineIOAuthResource(TimelineIORequestMixin):
    def login(self, email, password):
        data = {
            'email': email,
            'password': password,
        }
        return self._request(requests.post, self.get_full_endpoint('/api/auth/login'), data=data)
