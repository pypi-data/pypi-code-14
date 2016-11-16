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

    def post(self, original, response, *args, **kwargs):
        """ Set headers
        """
        try:
            for header_name, header_value in self.values:
                response[header_name] = header_value
        except Exception:
            LOGGER.warning("An error occured", exc_info=True)

        return {}
