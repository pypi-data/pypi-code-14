from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.browser.generate_pathbar import GeneratePathbar
from ftw.referencewidget.testing import FTW_REFERENCE_FUNCTIONAL_TESTING
from ftw.referencewidget.tests.views.form import TestView
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from unittest2 import TestCase
import json


class TestGeneratePathbar(TestCase):
    layer = FTW_REFERENCE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.folder = create(Builder('folder'))
        self.lower_file = create(Builder('file').within(
            self.folder).titled("Test"))
        self.file = create(Builder('file'))

    def test_generate_pathbar(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']
        view = GeneratePathbar(widget, widget.request)
        resultstr = view()
        result = json.loads(resultstr)
        self.assertEquals(1, len(result))
        self.assertEquals("/plone", result[0]['path'])
        self.assertEquals("Plone site", result[0]['title'])

    def test_generate_pathbar_multiple(self):
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        widget = form.form_instance.widgets['relation']

        widget.request['origin'] = '/plone/folder/test'
        view = GeneratePathbar(widget, widget.request)
        resultstr = view()
        result = json.loads(resultstr)
        self.assertEquals(3, len(result))
        self.assertEquals("/plone/folder/test", result[2]['path'])
        self.assertEquals("Test", result[2]['title'])
