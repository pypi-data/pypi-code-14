# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Record request context
"""
from logging import getLogger
from cgi import escape

from .regexp_rule import RegexpRule
from ..runtime_infos import runtime
from ..utils import is_string

LOGGER = getLogger(__name__)


class ReflectedXSSCB(RegexpRule):
    def post(self, original, _return, *args, **kwargs):
        """ Check if a template node returns a content that is in the
        query parameters
        """
        request = runtime.get_current_request()

        if not request:
            LOGGER.warning("No request was recorded abort")
            return

        if not is_string(_return):
            LOGGER.debug('Non string passed, type %s', type(_return))
            return

        if request.params_contains(_return):
            # If the payload is malicious, record the attack
            matching_regexp = self.match_regexp(_return)
            if matching_regexp:
                self.record_attack({'found': matching_regexp,
                                    'payload': _return})

            # Only if the callback should block, sanitize the string
            if self.should_block():
                return {'status': 'override', 'new_return_value': self._escape(_return)}

    def _escape(self, value):
        """ Escape a malicious value to make it safe
        """
        return escape(value, True)
