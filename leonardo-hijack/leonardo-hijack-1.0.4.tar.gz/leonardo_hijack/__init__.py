
from django.apps import AppConfig


default_app_config = 'leonardo_hijack.Config'


LEONARDO_ORDERING = -500

LEONARDO_APPS = [
    'leonardo_hijack',
    "hijack",
    "hijack_admin",
    "compat"
]

# LEONARDO_MIDDLEWARES = [
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'hijack.middleware.HijackRemoteUserMiddleware',
#     'django.contrib.auth.middleware.RemoteUserMiddleware',
# ]

LEONARDO_CSS_FILES = [
    'hijack/leonardo-hijack-styles.css'
]


class Config(AppConfig):
    name = 'leonardo_hijack'
    verbose_name = "leonardo-hijack"
