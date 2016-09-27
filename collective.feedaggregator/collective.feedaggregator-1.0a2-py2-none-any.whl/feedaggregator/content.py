# -*- coding: utf-8 -*-
"""The Feed Aggregator content type.

Note that helper methods have to be outside the class because
acquisition chain is lost when using a multiprocessing pool.
"""
from collective.feedaggregator.config import INMEDIATE_PROFILING
from collective.feedaggregator.interfaces import IFeedAggregator
from collective.feedaggregator.logger import logger
from datetime import datetime
from multiprocessing import Pool
from operator import itemgetter
from plone.dexterity.content import Item
from profilehooks import timecall
from time import mktime
from zope.globalrequest import getRequest
from zope.interface import implementer

import feedparser
import itertools


def _to_datetime(struct_time):
    """Convert time into datetime."""
    try:
        return datetime.fromtimestamp(mktime(struct_time))
    except TypeError:
        return None


def _parse_feed(url):
    """Parse the feed in the specified URL.

    :param url: the URL of a feed
    :type url: str
    :returns: a list of feed entries as dictionaries
    :rtype: list
    """
    logger.debug('Parsing feed: ' + url)
    feed = feedparser.parse(url)

    # TODO: deal with timeouts as feedparser have this hardcoded
    #       see: http://stackoverflow.com/q/9772691/644075

    if feed.bozo:
        context = getRequest().get('ACTUAL_URL')
        logger.warn('Invalid feed {0} in {1}'.format(url, context))
        return []

    entries = []
    for entry in feed['entries']:
        # RSS entry dates are parsed to updated attributes only
        # we use the same value for both fields if needed
        modified = entry.get('updated_parsed', '')  # optional element
        published = entry.get('published_parsed', modified)
        entries.append(dict(
            author=entry.get('author', ''),  # optional element
            description=entry.get('description'),
            modified=_to_datetime(modified),
            published=_to_datetime(published),
            title=entry.get('title'),
            url=entry.get('link'),
        ))
    return entries


@implementer(IFeedAggregator)
class FeedAggregator(Item):

    """A feed aggregator."""

    @timecall(immediate=INMEDIATE_PROFILING)
    def results(self):
        """Return a list of items from all feeds. To speed up feed
        parsing, we create a pool of cpu_count processes to get the
        items in parallel. Results are limited and sorted by the
        selected key in the specified order.
        """
        pool = Pool()
        results = pool.map(_parse_feed, self.feeds)
        # results is a list of lists; we must flatten it
        # see: http://stackoverflow.com/a/406199
        results = list(itertools.chain.from_iterable(results))
        return sorted(
            results,
            key=itemgetter(self.sort_on),
            reverse=self.sort_reversed,
        )[:self.limit]
