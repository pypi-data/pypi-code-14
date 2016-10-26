"""
############################################
:mod:`pywebtools.testing` -- py.test plugins
############################################

The primary use point is the :func:`~pywebtools.testing.functional_tester`
fixture.

.. moduleauthor:: Mark Hall <mark.hall@work.room3b.eu>
"""
from __future__ import (absolute_import, division, print_function, unicode_literals)

import pytest

from pyramid.paster import get_app
from pyramid.request import Request
from webtest import TestApp


@pytest.yield_fixture
def app():
    """Fixture that provides a newly initialised pyramid application defined in "testing.ini"
    with an empty database.
    """
    # Create the application
    app = get_app('testing.ini')

    # Yield to the test
    yield app


class RequestTesterMixin(object):
    """The :class:`~pywebtools.testing.RequestTesterMixin` provides functionality for making requests
    via the :class:`~pywebtools.testing.FunctionalTester`.
    """

    def get_url(self, url, headers=None):
        """Send a GET request to the given ``url``.

        :param url: The url to request
        :type url: ``unicode``
        :param headers: Optional headers to send with the request
        :type headers: ``dict`` or ``list``
        """
        if headers:
            if isinstance(headers, dict):
                if 'Accept' not in headers:
                    headers['Accept'] = '*/*'
            elif isinstance(headers, list):
                if 'Accept' not in dict(headers):
                    headers.append(('Accept', '*/*'))
        else:
            headers = [('Accept', '*/*')]
        self._response = self._test.get(url, headers=headers, status='*')

    def has_text(self, text):
        """Check whether the last response contains the given ``text``.

        :param text: The text to look for
        :type text: ``unicode``
        """
        if self._response:
            assert text in self._response.body.decode('utf-8')
        else:
            assert False, 'No request sent'

    def has_status(self, status):
        if self._response:
            assert self._response.status_int == status,\
                'Response status is %s instead of %s' % (self._response.status_int, status)
        else:
            assert False, 'No request sent'


class FunctionalTester(RequestTesterMixin):
    """The :class:`~pywebtools.testing.FunctionalTester` provides an easy interface for running
    functional tests. It mixes in :class:`~pywebtools.testing.RequestTesterMixin` and
    :class:`~pywebtools.testing.DBTesterMixin` to provide the actual functionality.

    The :class:`~pywebtools.testing.FunctionalTester` should always be created via the
    :func:`~pywebtools.testing.functional_tester` fixture.
    """

    def __init__(self, app):
        self._app = app
        self._test = TestApp(app)
        self._response = None


@pytest.yield_fixture
def functional_tester(app):
    """Fixture that provides a :class:`~pywebtools.testing.FunctionalTester`.
    """
    tester = FunctionalTester(app)
    yield tester


@pytest.yield_fixture
def request(app):
    """Fixture that provides a :class:`~pyramid.request.Request` that is
    simulated to have requested http://localhost."""
    request = Request({'REQUEST_METHOD': 'GET',
                       'SCRIPT_NAME': '',
                       'PATH_INFO': '',
                       'QUERY_STRING': '',
                       'CONTENT_TYPE': '',
                       'CONTENT_LENGTH': '',
                       'SERVER_NAME': 'localhost',
                       'SERVER_PORT': '80',
                       'SERVER_PROTOCOL': 'HTTP/1.0',
                       'wsgi.version': (1, 0),
                       'wsgi.url_scheme': 'http',
                       'wsgi.input': '',
                       'wsgi.errors': '',
                       'wsgi.multithread': False,
                       'wsgi.multiprocess': False,
                       'wsgi.run_once': False})
    request.registry = app.registry
    yield request
