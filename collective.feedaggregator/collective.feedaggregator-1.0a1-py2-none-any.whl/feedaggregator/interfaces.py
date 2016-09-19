# -*- coding: utf-8 -*-
from collective.feedaggregator import _
from plone.supermodel import model
from urlparse import urlparse
from zope import schema
from zope.interface import Interface
from zope.interface import Invalid


class IAddOnLayer(Interface):

    """Add-on specific layer."""


def validate_feed_uri(feed):
    result = urlparse(feed)
    if not all([result.scheme, result.netloc]):
        raise Invalid(_(u'The feed URI is invalid: ') + feed)
    return True


class IFeedAggregator(model.Schema):

    """A feed aggregator."""

    feeds = schema.Set(
        title=_(u'Feeds'),
        description=_(u'A list of feed URIs to be processed, one per line.'),
        required=True,
        default=set(),
        value_type=schema.ASCIILine(
            title=_(u'URI'),
            constraint=validate_feed_uri,
        ),
    )

    sort_on = schema.TextLine(
        title=_(u'Sort on'),
        description=_(u'Sort the items on this index.'),
        required=False,
    )

    sort_reversed = schema.Bool(
        title=_(u'Reversed order'),
        description=_(u'Sort the items in reversed order.'),
        required=False,
    )

    limit = schema.Int(
        title=_(u'Limit'),
        description=_(u'Maximum number of items to be shown.'),
        required=False,
        default=100,
    )

    item_count = schema.Int(
        title=_(u'label_item_count', default=u'Item count'),
        description=_(u'Number of items that will be shown in one batch.'),
        required=False,
        default=30,
    )
