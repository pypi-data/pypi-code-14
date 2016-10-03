
from django.apps import AppConfig

default_app_config = 'leonardo_import_export.Config'


class Default(object):

    apps = [
        'import_export',
        'leonardo_import_export'
    ]

    requirements = [
        'https://github.com/michaelkuty/django-import-export/archive/feature/extra_fields.zip'
        '#django-import-export==0.5.2.dev0'
    ]


class Config(AppConfig, Default):
    name = 'leonardo_import_export'
    verbose_name = "Import & Export"


default = Default()
