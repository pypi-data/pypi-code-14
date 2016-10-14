import unittest
from pyramid import (
    testing,
    httpexceptions,
)
from webtest import TestApp

import pyramid_unicodedammit


class ExpectedException(Exception):
    pass


class IgnoredException(Exception):
    pass


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _makeApp(self, include_tween=True):
        if include_tween:
            self.config.include('pyramid_unicodedammit')
        app = self.config.make_wsgi_app()
        return TestApp(app)

    def test_no_qs(self):
        config = self.config

        def view(request):
            self.assertEqual(request.GET, {})
            return 'ok'

        config.add_view(view, name='', renderer='string')

        app = self._makeApp()

        resp = app.get('/')

        self.assertEqual(resp.body, b'ok')

    def test_simple_ascii(self):
        config = self.config

        def view(request):
            self.assertEqual(request.GET, {
                'foo': 'bar',
                'baz': 'garply',
            })
            return 'ok'

        config.add_view(view, name='', renderer='string')

        app = self._makeApp()

        resp = app.get('/?foo=bar&baz=garply')

        self.assertEqual(resp.body, b'ok')

    def test_kaboom(self):
        config = self.config

        def view(request):
            request.GET  # Access query string to trigger decode failure
            self.fail()
            return 'ok'

        config.add_view(view, name='', renderer='string')

        app = self._makeApp(include_tween=False)

        with self.assertRaises(UnicodeDecodeError):
            app.get('/?foo=O\x92Brien')

    def test_cp1252(self):
        config = self.config

        def view(request):
            self.assertEqual(request.GET, {
                'foo': u'O\u2019Brien',
            })
            return 'ok'

        config.add_view(view, name='', renderer='string')

        app = self._makeApp()

        resp = app.get('/?foo=O\x92Brien')

        self.assertEqual(resp.body, b'ok')
