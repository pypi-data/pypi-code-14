from flask import url_for
from fifty_flask.views.generic import GenericView, MimeTypeResponseMixin, \
    TemplateView
from tests.mixins import AppMixin
from unittest import TestCase


class XMLTestView(MimeTypeResponseMixin, GenericView):
    mimetype = 'text/xml'

    def get(self):
        return '<lift>clean and jerk</lift>'


class DefaultMimeTypeTestView(GenericView):

    def get(self):
        return '<html><body>test</body></html>'


class TemplateViewTest(MimeTypeResponseMixin, TemplateView):
    mimetype = 'text/xml'
    template_name = 'mimetypetest.xml'

    def get_context_data(self, **context):
        context = super(TemplateViewTest, self).get_context_data(**context)
        context['message'] = 'Well Hello'
        return context


class MimeTypeResponseTests(AppMixin, TestCase):

    def setUp(self):
        super(MimeTypeResponseTests, self).setUp()
        XMLTestView.add_url_rule(self.app, '/xml/', 'test_xml_mimetype')
        DefaultMimeTypeTestView.add_url_rule(self.app, '/html/', 'test_html_mimetype')
        TemplateViewTest.add_url_rule(self.app, '/template/', 'test_template')
        self.xml_rv = self.test_app.get(url_for('test_xml_mimetype'))
        self.html_rv = self.test_app.get(url_for('test_html_mimetype'))
        self.template_rv = self.test_app.get(url_for('test_template'))


    def test_xml_mimetype(self):
        self.assertEqual(self.xml_rv.status_code, 200)
        self.assertEqual(self.xml_rv.mimetype, 'text/xml')
        self.assertEqual(self.xml_rv.content_type, 'text/xml; charset=utf-8')

    def test_default_mimetype(self):
        self.assertEqual(self.html_rv.status_code, 200)
        self.assertEqual(self.html_rv.mimetype, 'text/html')
        self.assertEqual(self.html_rv.content_type, 'text/html; charset=utf-8')

    def test_template_mimetype(self):
        self.assertEqual(self.template_rv.status_code, 200)
        self.assertEqual(self.template_rv.mimetype, 'text/xml')
        self.assertEqual(self.template_rv.content_type, 'text/xml; charset=utf-8')
        self.assertTrue('Well Hello' in self.template_rv.data)
