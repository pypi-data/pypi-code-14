from flask import url_for
from fifty_flask.views.generic import CORSMixin, FormView
from tests.forms import PersonForm
from tests.mixins import AppMixin
from unittest import TestCase


class CORSTestFormView(CORSMixin, FormView):
    form_cls = PersonForm
    template_name = 'form.html'

    def get_form_kwargs(self):
        form_kwargs = super(CORSTestFormView, self).get_form_kwargs()
        form_kwargs.setdefault('csrf_enabled', False)
        return form_kwargs


class CORSResponseTests(AppMixin, TestCase):

    def setUp(self):
        super(CORSResponseTests, self).setUp()
        view_func = CORSTestFormView.add_url_rule(self.app, '/cors/', 'test_cors')

    def test_get_cors_view(self):
        with self.test_app:
            response = self.test_app.get(url_for('test_cors'))
            self.assertEquals(response.status_code, 200)
            self.assertEquals('*', response.headers.get('Access-Control-Allow-Origin'))
            self.assertEquals('true', response.headers.get('Access-Control-Allow-Credentials'))
            self.assertEquals('GET, POST, OPTIONS', response.headers.get('Access-Control-Allow-Methods'))

    def test_cors_options_view(self):
        with self.test_app:
            response = self.test_app.options(url_for('test_cors'))
            self.assertEquals(response.status_code, 200)
            self.assertEquals('*', response.headers.get('Access-Control-Allow-Origin'))
            self.assertEquals('true', response.headers.get('Access-Control-Allow-Credentials'))
            self.assertEquals('GET, POST, OPTIONS', response.headers.get('Access-Control-Allow-Methods'))
