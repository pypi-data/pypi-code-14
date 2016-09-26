from ftw.topics.interfaces import IBackReferenceCollector
from ftw.topics.testing import EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.dexterity.fti import DexterityFTI
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zope.component import getMultiAdapter
import transaction


class TestTopicSupportBehavior(TestCase):

    layer = EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        portal_types = getToolByName(self.portal, 'portal_types')

        fti = DexterityFTI('DxTopicSupport')
        fti.behaviors = (
            'plone.app.dexterity.behaviors.metadata.IBasic',
            'plone.app.content.interfaces.INameFromTitle',
            'ftw.topics.behavior.ITopicSupportSchema',)
        portal_types._setObject('DxTopicSupport', fti)
        fti.lookupSchema()

        transaction.commit()

        self.browser = Browser(self.layer['app'])
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.handleErrors = False

    def test_behavior(self):
        self.browser.open(self.portal.portal_url() + '/++add++DxTopicSupport')
        browse_field_name = 'form.widgets.ITopicSupportSchema.topics'

        self.browser.getControl(label='Title').value = 'My Object'
        self.browser.getControl(name=browse_field_name).value = '/plone/' \
            'topics/manufacturing/quality'
        self.browser.getControl(label='Save').click()

        obj = self.portal.get('my-object')
        agile = self.portal.get('topics').get('manufacturing').get(
            'quality')

        collector = getMultiAdapter((agile, self.request),
                                    IBackReferenceCollector)
        section, = collector()
        self.assertItemsEqual((obj,), section.get('objects'))
