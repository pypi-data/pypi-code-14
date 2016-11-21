from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NavConfig(AppConfig):
    name = 'cms.nav'
    verbose_name = _('Navigation')
