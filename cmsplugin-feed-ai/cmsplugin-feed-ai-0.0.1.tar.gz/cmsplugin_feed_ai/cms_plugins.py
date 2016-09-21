# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .feed import get_aggregated_profile_feed, SUPPORTED_SERVICES
from .models import ProfileFeedPluginConf
from .providers.exceptions import FeedException


class ProfileFeedPlugin(CMSPluginBase):
    name = _("Profile feed")
    module = _("Social Media")
    model = ProfileFeedPluginConf
    render_template = "cmsplugin_feed_ai/feed.html"

    def get_feed(self, limit_per_service):
        """
        Get social media feed aggregation according
        to plugin definition.
        """
        try:
            return get_aggregated_profile_feed(
                SUPPORTED_SERVICES,
                limit_per_service=limit_per_service
            )
        except FeedException:
            return []

    def render(self, context, plugin_conf, placeholder):
        feed = self.get_feed(plugin_conf.items_per_service)
        context.update({
            "feed": feed,
            "placeholder": placeholder,
        })
        return context

plugin_pool.register_plugin(ProfileFeedPlugin)
