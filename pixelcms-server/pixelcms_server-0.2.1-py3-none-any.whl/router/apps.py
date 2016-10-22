from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RouterConfig(AppConfig):
    name = 'cms.router'
    verbose_name = _('Router')
