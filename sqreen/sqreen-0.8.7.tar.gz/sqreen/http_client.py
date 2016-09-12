# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Low-level HTTP interaction with sqreen API
"""
import os
import json
from json import JSONEncoder
from datetime import datetime

import sqreen

from .exceptions import InvalidResponseContentType, InvalidJsonResponse
from .exceptions import StatusFailedResponse, InvalidStatusCodeResponse

try:
    # Python 2
    import urlparse
except ImportError:
    import urllib.parse as urlparse

HAS_URLLIB3 = True
try:
    from urllib3 import Retry, PoolManager
    from urllib3.util.request import make_headers
except ImportError:
    try:
        from sqreen.vendors.urllib3 import Retry, PoolManager
        from sqreen.vendors.urllib3.util.request import make_headers
    except ImportError:
        HAS_URLLIB3 = False


class SqreenJsonEncoder(JSONEncoder):
    """ Custom JsonEncoder which can handle datetime objects
    >>> from datetime import datetime
    >>> date = datetime(2016, 3, 22, 14, 43, 14, 742306)
    >>> json.dumps(date, cls=SqreenJsonEncoder)
    '"2016-03-22T14:43:14.742306"'
    >>> json.dumps(2 + 1j, cls=SqreenJsonEncoder)
    '"(2+1j)"'
    >>> class Fail(object):
    ...     def __repr__(self):
    ...         raise NotImplementedError("Oups")
    ...
    >>> f = Fail()
    >>> json.dumps(f, cls=SqreenJsonEncoder)
    '"instance of type <class \\'sqreen.http_client.Fail\\'>"'
    """

    def default(self, obj):  # pylint: disable=E0202

        if isinstance(obj, datetime):
            return obj.isoformat()

        # For unknows types, JSONEncoder will raise a TypeError, instead,
        # returns obj repr
        try:
            return repr(obj)
        # If failing, return a fallback string here with the class name
        except Exception:
            return "instance of type {}".format(repr(obj.__class__))


def where_crt():
    """ Returns the path of the bundled crt
    """
    current_file = os.path.split(__file__)[0]
    return os.path.join(current_file, 'ca.crt')


class Urllib3Connection(object):
    """ Class responsible for making http request to sqreen API,

    handle connection pooling, retry and inbound/outbound formatting
    """
    RETRY_CONNECT_SECONDS = 10
    RETRY_REQUEST_SECONDS = 10

    MAX_DELAY = 60 * 30

    RETRY_STATUS = {503, 504}
    RETRY = Retry(total=5, method_whitelist=False,
                  status_forcelist=RETRY_STATUS, backoff_factor=1)
    RETRY_LONG = Retry(total=128, method_whitelist=False,
                       status_forcelist=RETRY_STATUS, backoff_factor=1)

    PATH_PREFIX = "/sqreen/v0/"

    def __init__(self, server_url):
        self.server_url = server_url
        self.parsed_server_url = urlparse.urlparse(server_url)

        if HAS_URLLIB3 is False:
            raise NotImplementedError("Couldn't find urllib3")
        self.connection = PoolManager(cert_reqs='CERT_REQUIRED',
                                      ca_certs=where_crt())

        user_agent = "sqreen/py-{}".format(sqreen.__version__)
        self.base_headers = make_headers(keep_alive=True, accept_encoding=True,
                                         user_agent=user_agent)

    def _url(self, url):
        """ Format and return an url based on instance path prefix
        """
        path = urlparse.urljoin(self.PATH_PREFIX, url)
        return urlparse.urlunparse((self.parsed_server_url[
            0], self.parsed_server_url[1], path, None, None, None))

    def post(self, endpoint, data=None, headers=None, retries=None):
        """ Post a request to the backend
        """
        url = self._url(endpoint)

        if headers is None:
            headers = {}

        if data is not None:
            data = json.dumps(data, separators=(',', ':'), cls=SqreenJsonEncoder)
            headers['Content-Type'] = 'application/json'

        # Add base headers
        headers.update(self.base_headers)

        response = self.connection.urlopen('POST',
                                           url,
                                           headers=headers,
                                           body=data,
                                           retries=retries)

        return self._parse_response(response)

    def get(self, endpoint, headers=None, retries=None):
        """ Get an endpoint in the backend
        """
        url = self._url(endpoint)

        if headers is None:
            headers = {}

        # Add base headers
        headers.update(self.base_headers)

        response = self.connection.urlopen('GET',
                                           url,
                                           headers=headers,
                                           retries=retries)

        return self._parse_response(response)

    def _parse_response(self, response):
        """ Try to decode response body to json
        """
        if response.status < 200 or response.status > 300:
            raise InvalidStatusCodeResponse(response.status, response.data)

        if response.headers.get('Content-Type') != 'application/json':
            raise InvalidResponseContentType(response.headers.get('Content-Type'))

        try:
            json_response = json.loads(response.data.decode('utf-8'))
        except ValueError as exc:
            raise InvalidJsonResponse(exc)

        if json_response.get('status', False) is False:
            raise StatusFailedResponse(json_response)

        return json_response
