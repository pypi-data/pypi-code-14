import os
from StringIO import StringIO
from fifty_flask.views.generic import SendFileView
from flask import current_app, url_for
from tests.mixins import AppMixin
from unittest import TestCase


class HtmlMimetypeMixin(object):
    mimetype = 'text/html'


class InlineFilenameView(SendFileView):
    as_attachment = False
    filename_or_fp = 'files/file'


class InlineFPView(SendFileView):
    as_attachment = False

    def get_filename_or_fp(self):
        return open(os.path.join(current_app.root_path, 'files/file'))


class InlineMimetypeView(HtmlMimetypeMixin, InlineFilenameView):
    pass


class AttachmentFilenameView(SendFileView):
    as_attachment = True
    filename_or_fp = 'files/file'


class AttachmentFilenameOverrideView(AttachmentFilenameView):
    attachment_filename = 'myfile'


class AttachmentMimetypeView(HtmlMimetypeMixin, AttachmentFilenameView):
    pass


class StringIOView(SendFileView):
    attachment_filename = 'file'

    def get_filename_or_fp(self):
        with open(os.path.join(current_app.root_path, 'files/file')) as f:
            return StringIO(f.read())


class SendFileTests(AppMixin, TestCase):
    def setUp(self):
        super(SendFileTests, self).setUp()
        self.file_content = 'file content'
        InlineFilenameView.add_url_rule(self.app, '/inline-filename/', 'inline_filename')
        InlineFPView.add_url_rule(self.app, '/inline-fp/', 'inline_fp')
        InlineMimetypeView.add_url_rule(self.app, '/inline-mimetype/', 'inline_mimetype')
        AttachmentFilenameView.add_url_rule(self.app, '/attachment-filename/', 'attachment_filename')
        AttachmentFilenameOverrideView.add_url_rule(self.app, '/attachment-filename-override/',
                'attachment_filename_override')
        StringIOView.add_url_rule(self.app, '/sio/', 'sio')
        AttachmentMimetypeView.add_url_rule(self.app, '/attachment-mimetype/',
                'attachment_mimetype')

    def test_inline_filename(self):
        """Serve file inline.
        """
        response = self.test_app.get(url_for('inline_filename'))
        self.assertIsInline(response)
        self.assertEqual(response.data.strip(), self.file_content)

    def test_inline_fp(self):
        """Serve file from file pointer inline.
        """
        response = self.test_app.get(url_for('inline_fp'))
        self.assertIsInline(response)
        self.assertEqual(response.data.strip(), self.file_content)

    def test_inline_mimetype(self):
        """Serve file inline with custom mimetype.
        """
        response = self.test_app.get(url_for('inline_mimetype'))
        self.assertIsInline(response)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.data.strip(), self.file_content)

    def test_attachment(self):
        """Serve file as attachemnt.
        """
        response = self.test_app.get(url_for('attachment_filename'))
        self.assertIsAttachment(response)
        self.assertEqual(response.data.strip(), self.file_content)

    def test_attachment_override(self):
        """Serve file as attachment with custom name.
        """
        response = self.test_app.get(url_for('attachment_filename_override'))
        self.assertHasFilename(response, 'myfile')
        self.assertEqual(response.data.strip(), self.file_content)

    def test_attachment_mimetype(self):
        """Serve file as attachment with custom mimetype.
        """
        response = self.test_app.get(url_for('attachment_mimetype'))
        self.assertIsAttachment(response)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.data.strip(), self.file_content)

    def test_sio(self):
        """Serve string as attachment using StringIO.
        """
        response = self.test_app.get(url_for('sio'))
        self.assertIsAttachment(response)
        self.assertEqual(response.data.strip(), self.file_content)

    def assertIsAttachment(self, response):
        """Asserts the response has an attachment.
        """
        content_disposition = response.headers.get('Content-Disposition')
        self.assertIsNotNone(content_disposition)
        self.assertTrue(content_disposition.startswith('attachment;'))

    def assertIsInline(self, response):
        """Asserts the response is not served as an attachment.
        """
        self.assertIsNone(response.headers.get('Content-Disposition'))

    def assertHasFilename(self, response, filename):
        """Asserts the response has a specific filename.
        """
        self.assertIsAttachment(response)
        content_disposition = response.headers.get('Content-Disposition')
        self.assertTrue(content_disposition.endswith('filename={}'.format(filename)))
