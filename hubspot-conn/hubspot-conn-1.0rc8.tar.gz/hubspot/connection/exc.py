##############################################################################
#
# Copyright (c) 2014, 2degrees Limited.
# All Rights Reserved.
#
# This file is part of hubspot-connection
# <https://github.com/2degrees/hubspot-connection>, which is subject to the
# provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

from httplib import NOT_FOUND as HTTP_NOT_FOUND
HTTP_TOO_MANY_REQUESTS = 429

class HubspotException(Exception):
    """The base HubSpot error."""
    pass


class HubspotUnsupportedResponseError(HubspotException):
    pass


class HubspotClientError(HubspotException):
    """
    HubSpot deemed the request invalid. This represents an HTTP response code
    of 40X, except 401

    :param unicode request_id:
    :param int http_status_code:

    """
    def __init__(self, msg, request_id, http_status_code=None):
        super(HubspotClientError, self).__init__(msg)

        self.request_id = request_id
        self.http_status_code = http_status_code

    @property
    def is_not_found(self):
        return self.http_status_code == HTTP_NOT_FOUND

    @property
    def is_too_many_requests(self):
        return self.http_status_code == HTTP_TOO_MANY_REQUESTS


class HubspotAuthenticationError(HubspotClientError):
    """
    HubSpot rejected your authentication key. This represents an HTTP
    response code of 401.

    """
    pass


class HubspotServerError(HubspotException):
    """
    HubSpot failed to process the request due to a problem at their end. This
    represents an HTTP response code of 50X.

    :param int http_status_code:

    """
    def __init__(self, msg, http_status_code):
        super(HubspotServerError, self).__init__(msg)

        self.msg = msg
        self.http_status_code = http_status_code

    def __repr__(self):
        return '{} {}'.format(self.http_status_code, self.msg)

