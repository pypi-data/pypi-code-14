# -*- coding: utf-8 -*-
from __future__ import absolute_import

from dateutil.parser import parse as parse_datetime
from facebook import GraphAPI, GraphAPIError

from ..utils import get_feed_settings
from .common import FeedDisplayItem
from .exceptions import FeedException


class FacebookFeedDisplayItem(FeedDisplayItem):
    source = "facebook"
    service_url = "https://facebook.com"

    def __init__(self, feed_obj, profile_name):
        """
        Initialize display item from raw facebook feed object provided by
        facebook API client (facebook-sdk).
        """
        super(FacebookFeedDisplayItem, self).__init__(profile_name)
        self.created_at = parse_datetime(feed_obj.get("created_time", ""))
        self.content_link = feed_obj.get("link", "")
        self.source_id = feed_obj.get("id", "")
        self.text_content = feed_obj.get(
            "message",
            feed_obj.get("status_type", "").replace("_", " ").capitalize
        )

    @property
    def permalink(self):
        """
        Permalink which points to the original feed object in external service.
        """
        return "%s/posts/%s" % (self.profile_url, self.source_id.split("_")[-1])


def fetch_profile_feed(profile_name, limit):
    """
    Fetch Facebook posts made by the profile defined in settings.
    Docs: https://developers.facebook.com/docs/graph-api/reference/v2.7/user/feed
    """
    api = GraphAPI(access_token=get_feed_settings("facebook")["auth_token"])
    try:
        return api.get_object(
            "%s/posts" % (profile_name),
            limit=limit,
            fields="id,created_time,message,link,status_type",
        )["data"]
    except GraphAPIError as e:
        raise FeedException(e)
