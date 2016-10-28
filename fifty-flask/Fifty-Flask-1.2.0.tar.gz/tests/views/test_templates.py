from fifty_flask.views.generic import TemplateResponseMixin, TemplateMixin, TemplateView
from flask import url_for
from tests.mixins import AppMixin
from unittest import TestCase


class BasicTemplateResponse(TemplateResponseMixin):
    template_name = 'basic.html'


class ContextTemplateResponse(TemplateMixin):
    template_name = 'with_context.html'

    def get_context_data(self, **context):
        context = super(ContextTemplateResponse, self).get_context_data(**context)
        context['name'] = 'flask'
        return context


class MyTemplateView(TemplateView):
    template_name = 'basic.html'


class MyTemplateContextView(TemplateView):
    template_name = 'with_context.html'

    def get_context_data(self, **context):
        context = super(MyTemplateContextView, self).get_context_data(**context)
        context['name'] = 'flask'
        return context


class TemplateTests(AppMixin, TestCase):
    def setUp(self):
        super(TemplateTests, self).setUp()
        MyTemplateView.add_url_rule(self.app, '/template', 'template')
        MyTemplateContextView.add_url_rule(self.app, '/template-context', 'template_context')

    def test_render_template(self):
        """Render a template using a mixin.
        """
        btr = BasicTemplateResponse()
        response = btr.render_response()
        self.assertEqual(response, 'basic template')

    def test_render_template_context(self):
        """Render a template with context using a mixin.
        """
        ctr = ContextTemplateResponse()
        context = ctr.get_context_data()
        response = ctr.render_response(**context)
        self.assertEqual(response, 'hello flask')

    def test_template_view(self):
        """A view that renders a template response.
        """
        response = self.test_app.get(url_for('template'))
        self.assertEqual(response.data, 'basic template')

    def test_template_view_context(self):
        """A view that renders a template response with context.
        """
        response = self.test_app.get(url_for('template_context'))
        self.assertEqual(response.data, 'hello flask')
