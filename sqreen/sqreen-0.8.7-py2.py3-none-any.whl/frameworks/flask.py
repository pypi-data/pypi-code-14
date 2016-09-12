# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Flask specific WSGI HTTP Request / Response stuff
"""

from itertools import chain
from logging import getLogger
from traceback import format_stack

try:
    # Python 2
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from .base import BaseRequest


LOGGER = getLogger(__name__)


class FlaskRequest(BaseRequest):

    def __init__(self, request):
        self.request = request

        # Convert django QueryDict to a normal dict with values as list
        self.converted_get = dict(self.request.args.lists())

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
        return dict(self.request.form)

    @property
    def cookies_params(self):
        return dict(self.request.cookies)

    @property
    def client_ip(self):
        access_route = self.request.access_route
        if len(access_route) == 0:
            return None
        return access_route[0]

    @property
    def hostname(self):
        parsed = urlparse.urlparse(self.request.url_root)
        return parsed.netloc

    @property
    def method(self):
        return self.request.method

    @property
    def referer(self):
        return self.request.referrer

    @property
    def client_user_agent(self):
        return self.request.user_agent.string

    @property
    def path(self):
        return self.request.full_path.rstrip('?')

    @property
    def scheme(self):
        return self.request.scheme

    @property
    def server_port(self):
        return self.request.environ.get('SERVER_PORT')

    @property
    def remote_port(self):
        return str(self.request.environ.get('REMOTE_PORT'))

    def get_header(self, name):
        """ Get a specific header
        """
        return self.request.environ.get(name)

    @property
    def caller(self):
        return format_stack()

    @property
    def view_params(self):
        return self.request.view_args
