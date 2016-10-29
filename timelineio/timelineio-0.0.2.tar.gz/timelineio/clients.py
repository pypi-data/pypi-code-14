# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from timelineio.resources import TimelineIOEventResource, TimelineIOCustomerResource


class TimelineIOClient(object):
    def __init__(self, base_api_url, auth_credentials=None, auth_token=None):
        self.base_api_url = base_api_url
        self.auth_credentials = auth_credentials
        self.auth_token = auth_token

    @property
    def base_resource_parameters(self):
        return {
            'base_api_url': self.base_api_url,
            'auth_credentials': self.auth_credentials,
            'auth_token': self.auth_token,
        }

    @property
    def Event(self):
        return TimelineIOEventResource(**self.base_resource_parameters)

    @property
    def Customer(self):
        return TimelineIOCustomerResource(**self.base_resource_parameters)
