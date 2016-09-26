# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Insert custom headers for Django
"""
import logging
from collections import Mapping

from ..rules import RuleCallback
from ..exceptions import InvalidArgument


LOGGER = logging.getLogger(__name__)


def convert_to_str(headers):
    """ Encode a list of headers tuples into latin1
    """
    for header_name, header_value in headers:
        header_name = str(header_name.encode('latin-1', errors='replace').decode('latin-1'))
        header_value = str(header_value.encode('latin-1', errors='replace').decode('latin-1'))
        yield (header_name, header_value)


class HeadersInsertCBDjango(RuleCallback):
    """ Callback that add the custom sqreen header
    """

    def __init__(self, *args, **kwargs):
        super(HeadersInsertCBDjango, self).__init__(*args, **kwargs)

        if not isinstance(self.data, Mapping):
            msg = "Invalid data type received: {}"
            raise InvalidArgument(msg.format(type(self.data)))

        try:
            self.values = self.data['values']
        except KeyError:
            msg = "No key 'values' in data (had {})"
            raise InvalidArgument(msg.format(self.data.keys()))

        self._headers = None

    @property
    def headers(self):
        """ Cached property to defer headers data conversion
        """
        if self._headers is None:
            self._headers = dict(convert_to_str(self.values))
        return self._headers

    def post(self, original, response, *args, **kwargs):
        """ Set headers
        """
        try:
            for header_name, header_value in self.headers.items():
                response[header_name] = header_value
        except Exception:
            LOGGER.warning("An error occured", exc_info=True)

        return {}
