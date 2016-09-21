# -*- coding: utf-8 -*-
from django.core.cache import cache

from .providers import facebook, twitter
from .utils import get_feed_settings

DEFAULT_CACHE_TIME = 3600  # 1 hour

SERVICE_TO_DISPLAY_ITEM_CLASS_MAP = {
    "facebook": facebook.FacebookFeedDisplayItem,
    "twitter": twitter.TwitterFeedDisplayItem,
}

SERVICE_TO_FETCHER_MAP = {
    "facebook": facebook.fetch_profile_feed,
    "twitter": twitter.fetch_profile_feed,
}

SUPPORTED_SERVICES = set(SERVICE_TO_DISPLAY_ITEM_CLASS_MAP.keys())


def _fetch_profile_feed(service, profile_name, limit):
    """
    Fetch profile feed from given service.
    :rtype: list[FeedDisplayItem]
    """
    return SERVICE_TO_FETCHER_MAP[service](profile_name, limit)


def get_profile_feed(service, profile_name, limit=5):
    """
    Get display ready profile feed from given service.
    This method uses cache to prevent excess calls to the service APIs.
    :param service: Service identifier
    :type service: Str
    :param limit: Amount of feed objects to be fetched per service
    :type limit: Int
    :rtype: [FeedDisplayItem]
    """
    key = "cmsplugin_feed_ai_%s_%s_%s" % (service, profile_name, str(limit))
    feed = cache.get(key)
    if not feed:
        feed = _fetch_profile_feed(service, profile_name, limit)
        cache.set(key, feed, get_feed_settings("cache_time", DEFAULT_CACHE_TIME))
    return [
        SERVICE_TO_DISPLAY_ITEM_CLASS_MAP[service](item, profile_name)
        for item in feed
    ]


def get_aggregated_profile_feed(services, limit_per_service=5):
    """
    Aggregate profile feeds from multiple services and
    sort the feed according to creation times.
    :param service: Service identifier
    :type service: Str
    :param limit: Amount of feed objects to be fetched per service
    :type limit: Int
    :rtype: [FeedDisplayItem]
    """
    aggregated_feed = []
    for service in services:
        profile_name = get_feed_settings(service)["profile_name"]
        aggregated_feed += get_profile_feed(service, profile_name, limit=limit_per_service)
    aggregated_feed.sort(key=lambda item: item.created_at, reverse=True)
    return aggregated_feed
