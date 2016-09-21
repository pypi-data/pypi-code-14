# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = (
    "ProfileFeedPluginConf",
)


class ProfileFeedPluginConf(CMSPlugin):
    """
    Plugin model for storing profile feed
    related configuration.
    """
    items_per_service = models.PositiveSmallIntegerField(
        default=5,
        verbose_name=_("number of items per service"),
    )

    def __str__(self):
        return "items per service: %s" % self.items_per_service
