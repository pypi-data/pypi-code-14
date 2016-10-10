
from django.apps import AppConfig


default_app_config = 'leonardo_hijack.Config'


LEONARDO_URLS_CONF = "hijack.urls"

LEONARDO_ORDERING = -500

LEONARDO_APPS = [
    'leonardo_hijack',
    "hijack",
    "compat"
]

LEONARDO_MIDDLEWARES = [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hijack.middleware.HijackRemoteUserMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
]


class Config(AppConfig):
    name = 'leonardo_hijack'
    verbose_name = "leonardo-hijack"
