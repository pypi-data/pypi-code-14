from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LiveAdminConfig(AppConfig):
    name = 'cms.live_admin'
    verbose_name = _('Live admin')
