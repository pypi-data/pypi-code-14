from ftw.builder import Builder
from ftw.builder import create
from ftw.referencewidget.browser.search import SearchView
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
        self.folder = create(Builder('folder').titled("Testfolder"))
        self.lower_file = create(Builder('file').within(
            self.folder).titled("Test"))
        self.file = create(Builder('file').titled("Sch\xc3\xbctzenpanzer"))
        form = TestView(self.portal, self.portal.REQUEST)
        form.update()
        self.widget = form.form_instance.widgets['relation']

    def test_search_view(self):
        self.widget.request['term'] = 'tes'
        view = SearchView(self.widget, self.widget.request)
        result = view()
        results = json.loads(result)
        items = results['items']
        self.assertEquals(2, len(items))
        self.assertEquals("/plone/testfolder", items[1]['path'])
        self.assertEquals("Testfolder (/plone/testfolder)", items[1]['title'])

        self.assertEquals("/plone/testfolder/test", items[0]['path'])
        self.assertEquals("Test (/plone/testfolder/test)", items[0]['title'])

    def test_only_correct_types(self):
        self.widget.override = True
        self.widget.selectable = ["Folder"]
        self.widget.request['term'] = 'tes'
        view = SearchView(self.widget, self.widget.request)
        result = view()
        results = json.loads(result)
        items = results['items']
        self.assertEquals(1, len(items))
        self.assertEquals("/plone/testfolder", items[0]['path'])
        self.assertEquals("Testfolder (/plone/testfolder)", items[0]['title'])
