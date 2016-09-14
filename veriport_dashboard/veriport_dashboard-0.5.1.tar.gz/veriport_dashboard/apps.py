from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VeriportDashboardConfig(AppConfig):
    name = 'veriport_dashboard'
    verbose_name = _("Veriport Dashboard")
