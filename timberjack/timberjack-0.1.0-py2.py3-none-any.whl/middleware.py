# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from . import get_logger
from . import utils
from . import events


class LoggingMiddleware(object):
    """
    Create a unique request ID and add a logger to the request object.

    The `RequestIDMiddleware` sets a unique ID for every request. The ID is
    either taken from the request headers (e.g. if passed by NGINX) or a new
    ID is generated using `uuid.UUID4`.
    """

    def process_request(self, request):
        """
        Create a `structlog` logger and add it as new request attribute.

        Note: adding a new attribute to the request will cause the `vary` header
        for the request to be set if the middleware is included **after** the
        `CsrfViewMiddleware`.
        """
        log = get_logger('brain.request')
        request.log = log.bind(user=utils.get_username_from_request(request))

        if hasattr(request, 'id'):
            request.log = log.bind(request_id=request.id)

        request.log.info(events.NEW_REQUEST_RECEIVED,
                         path=request.path_info,
                         session_id=request.session.session_key,
                         client_ip=utils.get_client_ip(request))
