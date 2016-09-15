
from django.apps import AppConfig
from leonardo_feature_switcher.base import is_off, is_on

default_app_config = 'leonardo_feature_switcher.Config'


LEONARDO_APPS = ['leonardo_feature_switcher']


LEONARDO_FEATURE_SWITCHERS = {}


class Config(AppConfig):
    name = 'leonardo_feature_switcher'
    verbose_name = "leonardo-feature-switcher"
