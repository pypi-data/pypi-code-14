# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from timberjack.compat import mock
from timberjack.middleware import LoggingMiddleware


def test_logging_middleware_creates_logger(rf):
    request = rf.get('/')
    request.session = mock.Mock(session_key='randomsessionkey')

    LoggingMiddleware().process_request(request)

    assert hasattr(request, 'log')
