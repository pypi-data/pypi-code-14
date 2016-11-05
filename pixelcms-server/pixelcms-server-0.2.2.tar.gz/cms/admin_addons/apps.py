from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AdminAddonsConfig(AppConfig):
    name = 'cms.admin_addons'
    verbose_name = _('Admin addons')
