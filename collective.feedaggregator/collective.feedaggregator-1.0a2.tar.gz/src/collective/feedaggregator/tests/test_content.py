# -*- coding: utf-8 -*-
from collective.feedaggregator.interfaces import IFeedAggregator
from collective.feedaggregator.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.f1 = api.content.create(
                self.portal, 'Feed Aggregator', 'f1')

    def test_adding(self):
        self.assertTrue(IFeedAggregator.providedBy(self.f1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Feed Aggregator')
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Feed Aggregator')
        schema = fti.lookupSchema()
        self.assertEqual(IFeedAggregator, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Feed Aggregator')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IFeedAggregator.providedBy(new_object))

    def test_is_selectable_as_folder_default_view(self):
        self.portal.setDefaultPage('f1')
        self.assertEqual(self.portal.default_page, 'f1')
