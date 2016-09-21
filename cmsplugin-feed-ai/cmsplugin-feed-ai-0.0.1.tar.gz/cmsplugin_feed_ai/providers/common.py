# -*- coding: utf-8 -*-
class FeedDisplayItem(object):
    created_at = None
    content_link = ""
    html_content = ""
    profile_name = ""
    service_url = ""
    source = ""
    source_id = ""
    text_content = ""

    def __init__(self, profile_name):
        """
        Initialize display item from raw feed object provided by
        service specific API tool.
        """
        self.profile_name = profile_name

    def __str__(self):
        return "%s %s" % (self.source, self.text_content[:20])

    def __repr__(self):
        return "<%s {'source': %s, 'text_content': %s, 'created_at': %s}>" % (
            type(self).__name__,
            self.source,
            self.text_content,
            self.created_at
        )

    @property
    def profile_url(self):
        """
        URL which points to the profile related to this feed item.
        """
        return "%s/%s" % (self.service_url, self.profile_name)

    @property
    def link(self):
        return self.content_link or self.permalink
