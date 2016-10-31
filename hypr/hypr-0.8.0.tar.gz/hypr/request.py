# Copyright 2014-2016 Morgan Delahaye-Prat. All Rights Reserved.
#
# Licensed under the Simplified BSD License (the "License");
# you may not use this file except in compliance with the License.
"""Request and related classes."""


import json
import asyncio

from datetime import datetime

from aiohttp import hdrs
from aiohttp.abc import AbstractMatchInfo
from aiohttp.protocol import HttpVersion11
from aiohttp.web import HTTPException, StreamResponse, \
    RequestHandler as BaseRequestHandler
from aiohttp.web_reqrep import Request as BaseRequest


class Request(BaseRequest):
    """Contains all the information about an incoming HTTP request."""

    def __init__(self, *args, **kwargs):
        """Create a new Request."""
        super().__init__(*args, **kwargs)
        self._ref_time = datetime.utcnow()

    @property
    def ref_time(self):
        """Return a reference time set at the Request creation."""
        return self._ref_time

    @property
    def args(self):
        """Alternate spelling for `Request.GET`."""
        return self.GET

    @asyncio.coroutine
    def json(self, *, loader=json.loads):
        """Parse the request content as JSON."""
        body = yield from self.text()
        if body:
            return loader(body)
        return None


@asyncio.coroutine
def defaultExpectHandler(request):
    """Default handler for Except: 100-continue."""
    if request.version == HttpVersion11:
        request.transport.write(b'HTTP/1.1 100 Continue\r\n\r\n')


class RequestHandler(BaseRequestHandler):
    """The request handler is the centerpiece of the request processing."""

    @asyncio.coroutine
    def handle_request(self, message, payload):
        """process the request."""
        now = self._loop.time()
        app = self._app
        request = app.request_class(
            app, message, payload,
            self.transport, self.reader, self.writer,
            secure_proxy_ssl_header=self._secure_proxy_ssl_header)
        self._meth = request.method
        self._path = request.path

        try:
            match_info = yield from self._router.resolve(request)
            assert isinstance(match_info, AbstractMatchInfo), match_info

            resp = None
            request._match_info = match_info
            expect = request.headers.get(hdrs.EXPECT)
            if expect and expect.lower() == "100-continue":
                resp = yield from defaultExpectHandler(request)

            if resp is None:
                handler = match_info.handler
                for factory in reversed(self._middlewares):
                    handler = yield from factory(app, handler)
                resp = yield from handler(request)

            assert isinstance(resp, StreamResponse), \
                ("Handler {!r} should return response instance, "
                 "got {!r} [middlewares {!r}]").format(
                     match_info.handler, type(resp), self._middlewares)
        except HTTPException as exc:
            resp = exc

        resp_msg = resp.start(request)
        yield from resp.write_eof()

        # notify server about keep-alive
        self.keep_alive(resp_msg.keep_alive())

        # log request processing
        if app.logger:
            app.logger.info(
                '%s %s - %s (%.0f ms)',
                request.method, request.path_qs, resp.status,
                (self._loop.time() - now)*1000
            )

        yield from app.request_teardown()

        # for repr
        self._meth = 'none'
        self._path = 'none'
