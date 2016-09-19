# -*- coding: utf-8 -*-
from collective.cover.tiles.collection import CollectionTile
from collective.cover.tiles.collection import ICollectionTile
from collective.feedaggregator import _
from plone.app.uuid.utils import uuidToObject
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer

import random


class IFeedAggregatorTile(ICollectionTile):

    """A tile that shows entries from a feed aggregator."""


@implementer(IFeedAggregatorTile)
class FeedAggregatorTile(CollectionTile):

    """A tile that shows entries from a feed aggregator."""

    index = ViewPageTemplateFile('feedaggregator.pt')
    short_name = _(u'msg_short_name_feedaggregator', u'Feed Aggregator')

    def __call__(self):
        """Initialize configured_fields on each call."""
        self.configured_fields = self.get_configured_fields()
        return super(FeedAggregatorTile, self).__call__()

    def accepted_ct(self):
        return ['Feed Aggregator']

    def get_field_configuration(self, field):
        """Return a dict with the configuration of the field. This is a
        helper function to deal with the ugliness of the internal data
        structure.
        """
        fields = self.get_configured_fields()
        return [f for f in fields if f['id'] == field][0]

    @property
    def count(self):
        # TODO: validation must be made upstream
        field = self.get_field_configuration('number_to_show')
        return int(field.get('size', 5))

    @property
    def offset(self):
        # TODO: validation must be made upstream
        field = self.get_field_configuration('offset')
        return int(field.get('offset', 0))

    def title_tag(self, entry):
        field = self.get_field_configuration('title')
        tag, title, url = field['htmltag'], entry['title'], entry['url']
        return u"""
            <{tag}>
              <a href="{url}">{title}</a>
            </{tag}>
            """.format(tag=tag, title=title, url=url)

    def results(self):
        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)
        if obj is None:
            self.remove_relation()  # the referenced object was removed
            return []

        # we use the view method as a helper as it's already cached
        view = obj.restrictedTraverse('listing_view')
        results = view.results

        if self.data.get('random', False):
            # return a sample of the population
            size = min(self.count, len(results))
            return random.sample(results, size)

        # return a slice of the list
        start, end = self.offset, self.offset + self.count
        return results[start:end]
