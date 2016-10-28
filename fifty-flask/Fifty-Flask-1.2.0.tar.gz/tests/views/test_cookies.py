from fifty_flask.views.generic import TemplateView, SetCookiesMixin
from flask import url_for
from tests.mixins import AppMixin
from unittest import TestCase


class BasicTemplateResponseWithCookies(SetCookiesMixin, TemplateView):
    template_name = 'basic.html'

    def get_response_cookies(self, response):
        cookies = super(BasicTemplateResponseWithCookies, self).get_response_cookies(response)
        cookies.append({
            'key': 'testing',
            'value': 'cookie',
            'max_age': 60 * 60 * 24
        })
        return cookies


class CookiesTests(AppMixin, TestCase):

    def setUp(self):
        super(CookiesTests, self).setUp()
        BasicTemplateResponseWithCookies.add_url_rule(self.app, '/cookies', 'cookies')

    def test_template_view_with_cookies(self):
        """A view that renders a template response.
        """
        response = self.test_app.get(url_for('cookies'))
        cookie_headers = [hdr for hdr in response.headers if hdr[0] == 'Set-Cookie']
        self.assertEqual(len(cookie_headers), 1)
        cookie_str = cookie_headers[0][1]
        self.assertIn('testing=cookie;', cookie_str)
        self.assertIn('Max-Age=86400;', cookie_str)
