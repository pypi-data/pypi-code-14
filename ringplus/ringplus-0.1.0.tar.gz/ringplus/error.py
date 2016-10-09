"""Errors related to the Python RingPLus API wrapper."""

from __future__ import print_function

import six

# 200 OK

# 201 Created,

# 202 Accepted

# 204 No Content

# 400 Bad Request

# 401 Unauthorized

# 403 Forbidden

# 404 Not Found

# 422 Unprocessable Entity


class RingPlusError(Exception):
    """RingPlus Exception"""

    def __init__(self, reason, response=None, api_code=None):
        self.reason = six.text_type(reason)
        self.response = response
        self.api_code = api_code
        Exception.__init__(self, reason)

    def __str__(self):
        if self.api_code:
            return self.api_code + ' ' + self.reason
        else:
            return self.reason


def is_rate_limit_error_message(message):
    """Check if the supplied error message belongs to a rate limit error."""
    return isinstance(message, list) \
        and len(message) > 0 \
        and 'code' in message[0] \
        and message[0]['code'] == 88


class RateLimitError(RingPlusError):
    pass
