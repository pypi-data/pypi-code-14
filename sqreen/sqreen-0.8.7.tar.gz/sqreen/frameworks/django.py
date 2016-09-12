# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Django specific WSGI HTTP Request / Response stuff
"""
from itertools import chain
from logging import getLogger

from .base import BaseRequest


LOGGER = getLogger(__name__)


class DjangoRequest(BaseRequest):

    def __init__(self, request, view_func, view_args, view_kwargs):
        self.request = request
        self.view_func = view_func
        self.view_args = view_args
        self.view_kwargs = view_kwargs

        # Convert django QueryDict to a normal dict with values as list
        self.converted_get = dict(self.request.GET.lists())

    @property
    def query_params(self):
        return self.converted_get

    @property
    def query_params_values(self):
        """ Return only query values as a list
        """
        return list(chain.from_iterable(self.converted_get.values()))

    @property
    def form_params(self):
        return dict(self.request.POST)

    @property
    def cookies_params(self):
        return self.request.COOKIES

    @property
    def client_ip(self):
        if 'HTTP_X_FORWARDED_FOR' in self.request.META:
            return self.request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        return self.request.META.get('REMOTE_ADDR')

    @property
    def hostname(self):
        return self.request.get_host()

    @property
    def method(self):
        return self.request.method

    @property
    def referer(self):
        return self.request.META.get('HTTP_REFERER')

    @property
    def client_user_agent(self):
        return self.request.META.get('HTTP_USER_AGENT')

    @property
    def path(self):
        return self.request.get_full_path()

    @property
    def scheme(self):
        return self.request.scheme

    @property
    def server_port(self):
        return self.request.META.get('SERVER_PORT')

    @property
    def remote_port(self):
        return self.request.META.get('REMOTE_PORT')

    def get_header(self, name):
        """ Get a specific header
        """
        return self.request.META.get(name)

    @property
    def view_params(self):
        return self.view_kwargs
