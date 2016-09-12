# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Base Request class
"""

import logging
from traceback import format_stack

LOGGER = logging.getLogger(__name__)


class BaseRequest(object):

    @property
    def request_payload(self):
        """ Returns current request payload with the backend expected field
        name.
        """
        return {
            'addr': self.client_ip,
            'host': self.hostname,
            'verb': self.method,
            'referer': self.referer,
            'user_agent': self.client_user_agent,
            'path': self.path,
            'scheme': self.scheme,
            'port': self.server_port,
            'rport': self.remote_port,
        }

    @property
    def request_params(self):
        """ Returns all the inputs that are controllable by the user
        """
        return {
            'form': self.form_params,
            'query': self.query_params,
            'cookies': self.cookies_params,
            'other': self.view_params
        }

    def params_contains(self, param):
        """ Return True if the parameter given in input is present in the
        request inputs.
        """
        iteration = 0
        max_iterations = 100

        remaining_iterables = [self.request_params]

        while len(remaining_iterables) != 0:

            iteration += 1
            # If we have a very big or nested iterable, returns False
            if iteration >= max_iterations:
                return False

            iterable_value = remaining_iterables.pop(0)

            # If we get an iterable, add it to the list of remaining
            if isinstance(iterable_value, dict):
                remaining_iterables.extend(list(iterable_value.values()))
            elif isinstance(iterable_value, list):
                remaining_iterables.extend(iterable_value)
            else:
                if iterable_value == param:
                    return True

        return False

    @property
    def full_payload(self):
        """ Return request information in the format accepted by the backend
        """
        return {
            'request': self.request_payload,
            'params': self.request_params
        }

    @property
    def caller(self):
        return format_stack()
