from fifty_flask.views.generic import TemplateResponseMixin, TemplateView
from flask import request, url_for
from tests.mixins import AppMixin
from unittest import TestCase


class NoPjaxView(TemplateView):
    template_name = 'basic.html'


class PjaxView(NoPjaxView):
    pjax_template_name = 'pjax.html'


class OverridePjaxTemplateView(PjaxView):
    def get_context_data(self, **context):
        context = super(OverridePjaxTemplateView, self).get_context_data(**context)
        context['has_context'] = request.args.get('context') == '1'
        return context

    def get_pjax_template_name(self, **context):
        if context.get('has_context'):
            return 'pjax_context.html'
        return 'basic.html'


class PjaxTests(AppMixin, TestCase):
    def setUp(self):
        super(PjaxTests, self).setUp()
        PjaxView.add_url_rule(self.app, '/pjax', 'pjax')
        NoPjaxView.add_url_rule(self.app, '/no-pjax', 'no-pjax')
        OverridePjaxTemplateView.add_url_rule(self.app, '/override-pjax', 'override-pjax')
        self.headers = {'X-PJAX': 1, 'X-Pjax-Container': 'pjax-container'}

    def test_no_pjax_view(self):
        """Send PJAX headers to a view that doesn't explicitly handle PJAX.
        """
        response = self.test_app.get(url_for('no-pjax'), headers=self.headers)
        self.assertEqual(response.data, 'basic template')

    def test_pjax_view(self):
        """Render a PJAX-friendly response.
        """
        response = self.test_app.get(url_for('pjax'), headers=self.headers)
        self.assertEqual(response.data, 'pjax-container\npjax.html')

    def test_override_pjax_template_name(self):
        """Override the default pjax template.
        """
        response = self.test_app.get(url_for('override-pjax'), headers=self.headers)
        self.assertEqual(response.data, 'basic template')

    def test_override_context_pjax_template_name(self):
        """Override the default pjax template by looking at context.
        """
        response = self.test_app.get(url_for('override-pjax', context=1), headers=self.headers)
        self.assertEqual(response.data, 'thar be pjax context here')
