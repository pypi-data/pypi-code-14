from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.xlsxsaveadapter.tests import FunctionalTestCase
from openpyxl.reader.excel import load_workbook
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from StringIO import StringIO
import os


class TestXlsxAdapter(FunctionalTestCase):

    def setUp(self):
        super(TestXlsxAdapter, self).setUp()

        self.resources_path = os.path.join(os.path.dirname(__file__),
                                           'resources')

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.form = create(Builder('form folder'))
        self.form.manage_delObjects(['mailer'])
        self.adapter = create(Builder('xlsx data adapter')
                              .having(UseColumnNames=True)
                              .within(self.form))

    @browsing
    def test_xlsx_generation(self, browser):
        browser.login().visit(self.form)
        browser.fill({'Your E-Mail Address': 'email@horst.ch',
                      'Subject': u'The S\xfcbject',
                      'Comments': u'The C\xf6mments'}).submit()

        self.assertEquals([['email@horst.ch',
                            'The S\xc3\xbcbject',
                            'The C\xc3\xb6mments']],
                          [item for item in self.adapter.getSavedFormInput()])

        browser.visit(self.adapter, view='download')

        book = load_workbook(StringIO(browser.contents))
        sheet = book.active

        self.assertEquals(sheet['A1'].value, u'Your E-Mail Address')
        self.assertEquals(sheet['B1'].value, u'Subject')
        self.assertEquals(sheet['C1'].value, u'Comments')
        self.assertEquals(sheet['A2'].value, u'email@horst.ch')
        self.assertEquals(sheet['B2'].value, u'The S\xfcbject')
        self.assertEquals(sheet['C2'].value, u'The C\xf6mments')
        self.assertIsNone(sheet['D1'].value)
        self.assertIsNone(sheet['A3'].value)
