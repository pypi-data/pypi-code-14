from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmailsConfig(AppConfig):
    name = 'cms.emails'
    verbose_name = _('Emails')
