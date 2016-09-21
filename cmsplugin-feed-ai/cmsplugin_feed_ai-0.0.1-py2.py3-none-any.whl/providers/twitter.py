# -*- coding: utf-8 -*-
from dateutil.parser import parse as parse_datetime
from twython import Twython
from twython.exceptions import TwythonError

from ..utils import get_feed_settings
from .common import FeedDisplayItem
from .exceptions import FeedException


class TwitterFeedDisplayItem(FeedDisplayItem):
    source = "twitter"
    service_url = "https://twitter.com"

    def __init__(self, feed_obj, profile_name):
        """
        Initialize display item from raw Twitter feed object provided by
        Twitter API client (Twython).
        """
        super(TwitterFeedDisplayItem, self).__init__(profile_name)
        self.created_at = parse_datetime(feed_obj.get("created_at", ""))
        self.html_content = Twython.html_for_tweet(feed_obj)
        self.source_id = feed_obj.get("id_str", "")
        self.text_content = feed_obj.get("text", "")

    @property
    def permalink(self):
        """
        Permalink which points to the original feed object in external service.
        """
        return "%s/status/%s" % (self.profile_url, self.source_id)


def fetch_profile_feed(profile_name, limit):
    """
    Fetch Twitter feed for the profile defined in settings.
    Twython Docs: http://twython.readthedocs.io/en/latest/api.html?highlight=get_user_timeline#twython.Twython.get_user_timeline  # noqa
    Twitter Docs: https://dev.twitter.com/rest/reference/get/statuses/user_timeline
    """
    conf = get_feed_settings("twitter")
    api = Twython(
        app_key=conf["app_key"],
        app_secret=conf["access_token"],
    )
    try:
        return api.get_user_timeline(
            screen_name=profile_name,
            count=limit,
        )
    except TwythonError as e:
        raise FeedException(e)
