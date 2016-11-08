'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

import functools
import json
import sys
import time

import requests
import six
from typing import Optional  # noqa

from sxclient import exceptions
from sxclient.models import Cluster, QueryParameters  # noqa
from sxclient.query.cluster_session import ClusterSession  # noqa
from sxclient.query.utils import job_poll_params
from sxclient.tools import generate_poll_times


HTTP_STATUS_TO_EXCEPTIONS_MAP = {
    400: exceptions.SXClusterBadRequest,
    401: exceptions.SXClusterUnauthorized,
    403: exceptions.SXClusterForbidden,
    404: exceptions.SXClusterNotFound,
    408: exceptions.SXClusterRequestTimeout,
    410: exceptions.SXClusterNodeNotAMember,
    413: exceptions.SXClusterPayloadTooLarge,
    429: exceptions.SXClusterTooManyRequests,
}


class BaseQueryHandler(object):
    '''
    Prepare and send a query to an SX cluster.

    Initialization parameters (set as the attributes):
      - node_address -- address of the cluster's node to connect to
      - cluster -- Cluster data structure containing cluster's location
        data
      - session -- requests.Session-derived object used to send the
        requests

    Other attributes:
      - url -- actual URL used to connect to the node
      - cluster_uuid -- UUID of the cluster
      - timeout -- timeout set for requests being made
      - query -- latest sent query
      - response -- latest received response
      - poll_time_gen -- poll time generator; if replaced, should
        accept two arguments, start and end, and indefinitely yield the
        values from the interval bounded by start and end.

    This a base class that does not implement body serialization. Subclasses
    you can use are: JSONBodyQueryHandler, BinaryBodyQueryHandler.
    '''
    query = None  # type: requests.Request
    response = None  # type: requests.Response
    is_query_complex = None  # type: bool

    def __init__(self, node_address, cluster, session):
        # type: (str, Cluster, ClusterSession) -> None
        self.node_address = node_address
        self.cluster = cluster
        self.session = session
        self.timeout = session.request_timeout
        self.poll_time_gen = functools.partial(generate_poll_times, steps=10)

    @property
    def url(self):  # type: () -> str
        return self.cluster.get_host_url(self.node_address)

    def prepare_query(self, query_params, body=None):
        # type: (QueryParameters, Optional[dict]) -> None
        query = self._create_query(query_params, body)
        query.node_address = self.node_address  # type: ignore FIXME
        self.query = query

    def make_query(self):
        # type: () -> None
        if self.is_query_complex:
            self._make_complex_query()
        else:
            self._make_simple_query()

    def _make_simple_query(self):
        # type: () -> None
        self.response = self._send_request(
            self.query, self.session, self.timeout)

    def _make_complex_query(self):
        # type: () -> None
        resp = self._send_request(self.query, self.session, self.timeout)
        resp_body = resp.json()
        req_id = resp_body['requestId']
        min_time = resp_body['minPollInterval'] / 1000.0
        max_time = resp_body['maxPollInterval'] / 1000.0

        for period in self.poll_time_gen(min_time, max_time):
            time.sleep(period)
            resp = self._make_poll_query(req_id, timeout=self.timeout)
            self.response = resp
            resp_body = resp.json()
            status = resp_body['requestStatus']

            if status == 'PENDING':
                continue
            elif status == 'OK':
                break
            elif status == 'ERROR':
                resp_msg = resp_body['requestMessage']
                raise exceptions.SXClusterNonFatalError(resp_msg)
            else:
                raise exceptions.SXClusterNonFatalError(
                    'Invalid poll response status'
                )

    def _serialize_request_body(self, body):
        # type: (Optional[dict]) -> str
        raise NotImplementedError

    def _create_query(self, query_params, body=None):
        # type: (QueryParameters, Optional[dict]) -> requests.Request
        verb = query_params.verb
        self.is_query_complex = query_params.is_complex
        path = query_params.path
        params = query_params.params

        url = '/'.join([self.url, path])
        body_str = self._serialize_request_body(body)
        query = requests.Request(verb, url, params=params, data=body_str)
        query = self.session.prepare_request(query)
        query.node_address = self.node_address  # type: ignore FIXME
        return query

    def _make_poll_query(self, req_id, timeout=None):
        # type: (str, Optional[int]) -> requests.Response
        poll_query = self._create_query(job_poll_params(req_id))
        resp = self._send_request(poll_query,
                                  self.session,
                                  timeout=timeout)
        return resp

    @classmethod
    def _handle_http_error(cls, resp):
        # type: (requests.Response) -> None
        err_val, err_tb = sys.exc_info()[1:]
        try:
            resp_msg = resp.json()['ErrorMessage']
        except ValueError:
            resp_msg = ''

        exc = HTTP_STATUS_TO_EXCEPTIONS_MAP.get(resp.status_code)
        if exc is None:
            if 400 <= resp.status_code < 500:
                exc = exceptions.SXClusterClientError
            elif resp.status_code >= 500:
                exc = exceptions.SXClusterInternalError

        exc_message = '{} {}'.format(err_val, resp_msg).strip()
        six.reraise(exc, exc(exc_message), err_tb)

    @classmethod
    def validate_response(cls, resp):
        # type: (requests.Response) -> None
        pass

    @classmethod
    def _send_request(cls, req, session, timeout=None):
        # type: (requests.Request, ClusterSession, Optional[int]) -> requests.Response  # noqa
        '''
        Send 'requests.PreparedRequests', using session provided in the
        argument and raise error in case of failure.
        '''
        try:
            resp = session.send(req, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout):
            err_val, err_tb = sys.exc_info()[1:]
            six.reraise(
                exceptions.SXClusterNonFatalError,
                exceptions.SXClusterNonFatalError(err_val),
                err_tb,
            )

        resp.node_address = req.node_address  # type: ignore FIXME

        # Check whether the response status is valid.
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            cls._handle_http_error(resp)

        cls.validate_response(resp)

        # Check whether the response contains 'SX-Cluster' header.
        if 'sx-cluster' not in resp.headers:
            msg = "No 'SX-Cluster' header in the response"
            raise exceptions.SXClusterNonFatalError(msg)

        return resp


class JSONBodyQueryHandler(BaseQueryHandler):
    def _serialize_request_body(self, body):
        # type: (Optional[dict]) -> str
        return json.dumps(body) if body else ''

    @classmethod
    def validate_response(cls, resp):
        # type: (requests.Response) -> None
        # Check whether the response content is parseable into JSON.
        try:
            info = resp.json()
        except ValueError:
            err_val, err_tb = sys.exc_info()[1:]
            new_msg = '{}: {}'.format('Cannot parse JSON', err_val)
            six.reraise(
                exceptions.SXClusterNonFatalError,
                exceptions.SXClusterNonFatalError(new_msg),
                err_tb,
            )

        # Check whether there is an error message in parsed response content.
        if 'ErrorMessage' in info:
            raise exceptions.SXClusterNonFatalError(info['ErrorMessage'])


class BinaryBodyQueryHandler(BaseQueryHandler):
    def _serialize_request_body(self, body):
        # type: (bytes) -> bytes
        return body
