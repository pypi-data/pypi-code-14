from __future__ import unicode_literals

import numpy as np

from datetime import timedelta

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class ReportFilter(models.Model):
    """
    Stores filters to be used in :model:'veriport_dashboard.Report'
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
        related_name="saved_filters")
    name = models.CharField(max_length=255)
    start_date = models.CharField(max_length=32, blank=True,
        help_text=_("Date in string format MM/DD/YYYY."))
    end_date = models.CharField(max_length=32, blank=True,
        help_text=_("Date in string format MM/DD/YYYY."))
    data = JSONField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Report Filter")
        verbose_name_plural = _("Report Filters")

    def __str__(self):
        return "{0}: {1}".format(self.user, self.name)


@python_2_unicode_compatible
class SystemMessage(models.Model):
    """
    stores messages for users in the system
    """
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("System Message")
        verbose_name_plural = _("System Messages")

    def __str__(self):
        return "{0}".format(self.content)
