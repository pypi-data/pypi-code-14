from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SettingsConfig(AppConfig):
    name = 'cms.settings'
    verbose_name = _('Settings')
