
from django.apps import AppConfig

default_app_config = 'leonardo_import_export.Config'


class Default(object):

    apps = [
        'import_export',
        'leonardo_import_export'
    ]


class Config(AppConfig, Default):
    name = 'leonardo_import_export'
    verbose_name = "Import & Export"


default = Default()
