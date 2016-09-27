# -*- coding: utf-8 -*-
from collective.feedaggregator.config import TTL
from plone import api
from plone.memoize import ram
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


def _feedaggregator_cachekey(method, self):
    """Cache key to be used on Feed Aggregator intances.
    Besides the instance URL, it uses last modification time (to
    invalidate on changes) and a global TTL.
    """
    return (
        self.context.absolute_url(),  # feed aggregator instance
        str(self.context.modified()),  # last modification time
        TTL,  # time-to-live (15 minutes)
    )


class ListingView(BrowserView):

    """Default view, a listing of feed entries."""

    index = ViewPageTemplateFile('feedaggregator.pt')

    def __init__(self, context, request):
        super(ListingView, self).__init__(context, request)
        self.b_size = context.item_count
        b_start = getattr(request, 'b_start', 0)
        self.b_start = int(b_start)

    def __call__(self):
        return self.index()

    @property
    @ram.cache(_feedaggregator_cachekey)
    def results(self):
        return self.context.results()

    def batch(self):
        return Batch(
            self.results, size=self.b_size, start=self.b_start, orphan=1)

    @property
    def show_byline(self):
        # TODO
        return True

    def get_localized_time(self, datetime):
        """Convert time into localized time in long format."""
        return api.portal.get_localized_time(datetime, long_format=True)
