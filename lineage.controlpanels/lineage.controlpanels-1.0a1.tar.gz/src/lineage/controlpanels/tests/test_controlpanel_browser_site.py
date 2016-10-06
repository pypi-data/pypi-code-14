# -*- coding: utf-8 -*-
from ..testing import LINEAGE_CONTROLPANELS_INTEGRATION_TESTING
from collective.lineage.utils import enable_childsite
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from Products.CMFPlone.interfaces import ISiteSchema
from StringIO import StringIO
from zope.component import getUtility
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

import plone.api.content
import transaction
import unittest2 as unittest

# Red pixel with filename pixel.png
LOGO_1_BASE64 = 'filenameb64:cGl4ZWwucG5n;datab64:iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12P4z8AAAAMBAQAY3Y2wAAAAAElFTkSuQmCC'  # noqa

# Green pixel with filename pixelgreen.png
LOGO_2_BASE64 = 'filenameb64:cGl4ZWxncmVlbi5wbmc=;datab64:iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12Ng+M8AAAICAQCqKp4nAAAAAElFTkSuQmCC'  # noqa


class SiteControlPanelFunctionalTest(unittest.TestCase):
    """Test that changes in the site control panel are actually
    stored in the registry.
    """
    layer = LINEAGE_CONTROLPANELS_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        plone.api.content.create(
            container=self.portal,
            type='Folder',
            id='subsite',
            title='subsite'
        )
        self.subsite = self.portal['subsite']
        plone.api.content.transition(obj=self.subsite, transition='publish')
        enable_childsite(self.subsite)

    def _registry_edit(self, context, schema, data):
        """Edit data against the registry schema on a given context."""
        registry = getUtility(IRegistry, context=context)
        settings = registry.forInterface(schema, prefix="plone")
        for item in data:
            setattr(settings, item['name'], item['value'])

    def _registry_assert(self, context, schema, data):
        """Assert data against the registry schema on a given context."""
        registry = getUtility(IRegistry, context=context)
        settings = registry.forInterface(schema, prefix="plone")

        for item in data:
            self.assertEqual(getattr(settings, item['name']), item['value'])

    def test_lineage_controlpanel_site_roundtrip(self):
        """Test editing the main site controlpanel and the lineage controlpanel
        in a subsite and check, if settings don't overwrite each other.
        """
        data_portal = [
            {'name': 'site_title', 'value': u'Main portal'},
            {'name': 'site_logo', 'value': LOGO_1_BASE64},
            {'name': 'exposeDCMetaTags', 'value': True},
            {'name': 'enable_sitemap', 'value': True},
            {'name': 'webstats_js', 'value': u'// dummy js'},
            {'name': 'display_publication_date_in_byline', 'value': True},
            {'name': 'icon_visibility', 'value': u'enabled'},
            {'name': 'thumb_visibility', 'value': u'enabled'},
            {'name': 'toolbar_position', 'value': u'side'},
            {'name': 'toolbar_logo', 'value': u'some_logo, nonexistent'},
            {'name': 'robots_txt', 'value': u'please, no robots'},
            {'name': 'default_page', 'value': [u'start.html']},
            {'name': 'roles_allowed_to_add_keywords', 'value': [u'Manager']},
        ]

        data_subsite = [
            {'name': 'site_title', 'value': u'Sub portal'},
            {'name': 'site_logo', 'value': LOGO_2_BASE64},
            {'name': 'exposeDCMetaTags', 'value': True},
            {'name': 'enable_sitemap', 'value': True},
            {'name': 'webstats_js', 'value': None},
            {'name': 'display_publication_date_in_byline', 'value': True},
            {'name': 'icon_visibility', 'value': u'false'},
            {'name': 'thumb_visibility', 'value': u'false'},
            {'name': 'toolbar_position', 'value': u'side'},
            {'name': 'toolbar_logo', 'value': u'another nonexistent logo'},
            {'name': 'robots_txt', 'value': u'more robots!'},
            {'name': 'default_page', 'value': [u'start.html']},
            {'name': 'roles_allowed_to_add_keywords', 'value': [u'Manager']},
        ]

        # Populate main site
        self._registry_edit(self.portal, ISiteSchema, data_portal)

        # Populate child site
        self._registry_edit(self.subsite, ISiteSchema, data_subsite)

        # Assert main portal
        self._registry_assert(self.portal, ISiteSchema, data_portal)

        # Assert sub portal
        self._registry_assert(self.subsite, ISiteSchema, data_subsite)
