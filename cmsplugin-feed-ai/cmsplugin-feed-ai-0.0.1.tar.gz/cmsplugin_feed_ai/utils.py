# -*- coding: utf-8 -*-
from warnings import warn

from django.conf import settings


def get_feed_settings(key, default=None):
    feed_settings = getattr(settings, "AI_FEED_SETTINGS", {})
    if key not in feed_settings:
        warn("Missing %r setting in AI_FEED_SETTINGS" % key)
        return default
    return feed_settings.get(key, default)
