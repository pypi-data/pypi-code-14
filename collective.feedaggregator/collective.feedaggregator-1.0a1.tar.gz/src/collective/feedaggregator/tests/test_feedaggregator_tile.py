# -*- coding: utf-8 -*-
"""Tests in this module are executed only if collective.cover is installed."""
from collective.feedaggregator.testing import HAS_COVER
from collective.feedaggregator.testing import INTEGRATION_TESTING
from lxml import etree
from mock import Mock
from plone import api

import unittest

if HAS_COVER:
    from collective.cover.tests.base import TestTileMixin
    from collective.feedaggregator.tiles.feedaggregator import IFeedAggregatorTile
    from collective.feedaggregator.tiles.feedaggregator import FeedAggregatorTile
else:  # skip tests
    class TestTileMixin:
        pass

    def test_suite():
        return unittest.TestSuite()


class FeedAggregatorTileTestCase(TestTileMixin, unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        super(FeedAggregatorTileTestCase, self).setUp()
        self.tile = FeedAggregatorTile(self.cover, self.request)
        self.tile.__name__ = u'collective.feedaggregator'
        self.tile.id = u'test'

        with api.env.adopt_roles(['Manager']):
            self.feedaggregator = api.content.create(
                self.portal, 'Feed Aggregator', 'test', u'Lorem ipsum')

    @unittest.expectedFailure  # FIXME: raises BrokenImplementation
    def test_interface(self):
        self.interface = IFeedAggregatorTile
        self.klass = FeedAggregatorTile
        super(FeedAggregatorTileTestCase, self).test_interface()

    def test_default_configuration(self):
        self.assertTrue(self.tile.is_configurable)
        self.assertTrue(self.tile.is_editable)
        self.assertTrue(self.tile.is_droppable)

    def test_accepted_content_types(self):
        self.assertEqual(
            self.tile.accepted_ct(), ['Feed Aggregator'])

    def test_render_empty(self):
        msg = u'Drop a feed aggregator here to fill the tile.'

        self.tile.is_compose_mode = Mock(return_value=True)
        self.assertIn(msg, self.tile())

        self.tile.is_compose_mode = Mock(return_value=False)
        self.assertNotIn(msg, self.tile())

    def test_render(self):
        self.tile.populate_with_object(self.feedaggregator)
        html = etree.HTML(self.tile())
        self.assertIn(u'Lorem ipsum', html.xpath('//h2/text()'))  # header
        # TODO: mock feed
        self.assertIn(u'More…', html.xpath('//div/a/text()'))  # footer

    def test_render_no_entries(self):
        msg = u'There are currently no entries in this feed aggregator.'
        self.tile.populate_with_object(self.feedaggregator)
        html = etree.HTML(self.tile())
        self.assertIn(msg, html.xpath('//p/text()'))

    def test_render_deleted_object(self):
        self.tile.populate_with_object(self.feedaggregator)
        api.content.delete(self.feedaggregator)
        # tile's data is cached; reinstantiate it
        self.tile = self.cover.restrictedTraverse('@@collective.feedaggregator/test')
        self.assertIsInstance(self.tile(), unicode)  # no error on rendering

    @unittest.expectedFailure  # FIXME: mock feed
    def test_alt_atribute_present_in_images(self):
        raise NotImplemented
