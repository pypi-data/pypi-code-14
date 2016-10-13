
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

default_app_config = 'leonardo_store_faq.Config'


LEONARDO_APPS = ['leonardo_store_faq']


class Config(AppConfig):
    name = 'leonardo_store_faq'
    verbose_name = _("Store FAQ")
