import urlparse

import ujson

from bedlam.errors import PayloadError, BedlamError


class Request(object):
    def __init__(self, environ):
        self._uri = environ['RAW_URI']
        self._path = environ['PATH_INFO'].strip('/')
        self._method = environ['REQUEST_METHOD']
        self._remote_addr = environ['REMOTE_ADDR']

        _query_string = environ['QUERY_STRING']
        self._query_params = QueryParams(_query_string)

        _wsgi_input = environ['wsgi.input']
        self._request_body = RequestBody(_wsgi_input)

    @property
    def uri(self):
        return self._uri

    @property
    def path(self):
        return self._path

    @property
    def method(self):
        return self._method

    @property
    def query_params(self):
        return self._query_params

    @property
    def body(self):
        return self._request_body


class QueryParams(object):
    def __init__(self, query_string):
        self._query_string = query_string
        query_params = urlparse.parse_qsl(query_string)
        self._query_params = dict(query_params)

    @property
    def raw(self):
        return self._query_string

    @property
    def as_dict(self):
        return self._query_params

    def __getitem__(self, key):
        return self._query_params.get(key)

    def __getattr__(self, key):
        return self._query_params.get(key)


class RequestBody(object):
    def __init__(self, wsgi_input):
        self._body = wsgi_input.read()
        self._deserialized = self._deserialize(self._body)

    @staticmethod
    def _deserialize(body):
        if not body:
            return {}

        try:
            body = ujson.loads(body)
        except ValueError as err:
            raise PayloadError(err)
        except:
            raise BedlamError

        if not body:
            return {}

        # if not isinstance(body, dict):
        #     raise PayloadError

        return body

    @property
    def raw(self):
        return self._body

    def __getitem__(self, key):
        return self._deserialized.get(key)

    def __getattr__(self, key):
        return self._deserialized.get(key)

    def __iter__(self):
        return self._deserialized.iteritems()
        # for k, v in self._deserialized.iteritems():
        #     yield k, v

    def __contains__(self, key):
        return key in self._deserialized
