from fifty_flask.views.generic import GenericView, RedirectView
from flask import request, url_for
from tests.mixins import AppMixin
from unittest import TestCase
from urlparse import urlparse


class RedirectView1(RedirectView):
    pass


class RedirectView2(RedirectView):
    redirect_endpoint = 'lander'


class RedirectView3(RedirectView2):
    def get_context_data(self, **context):
        context = super(RedirectView3, self).get_context_data(**context)
        context['a'] = 'b'
        return context


class LanderView(GenericView):
    def get(self, *args, **kwargs):
        return 'landed'


class RedirectTests(AppMixin, TestCase):
    def setUp(self):
        super(RedirectTests, self).setUp()
        RedirectView1.add_url_rule(self.app, '/redirect1/', 'redirect1')
        RedirectView2.add_url_rule(self.app, '/redirect2/', 'redirect2')
        RedirectView3.add_url_rule(self.app, '/redirect3/', 'redirect3')
        LanderView.add_url_rule(self.app, '/lander/', 'lander')

    def test_redirect1(self):
        """Redirect to self.
        """
        response = self.test_app.get(url_for('redirect1'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, url_for('redirect1', _external=True))

    def test_redirect2(self):
        """Redirect to another route.
        """
        response = self.test_app.get(url_for('redirect2'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, url_for('lander', _external=True))

    def test_redirect3(self):
        """Redirect to another route, passing query string parameters.
        """
        response = self.test_app.get(url_for('redirect3'))
        self.assertEqual(response.status_code, 302)

        parsed_url = urlparse(response.location)
        location = '{scheme}://{host}{path}' \
                .format(scheme=parsed_url.scheme, host=parsed_url.netloc, path=parsed_url.path)
        self.assertEqual(location, url_for('lander', _external=True))
        self.assertEqual(parsed_url.query, 'a=b')
