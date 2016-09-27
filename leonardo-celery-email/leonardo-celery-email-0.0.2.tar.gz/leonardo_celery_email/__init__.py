
from django.apps import AppConfig

default_app_config = 'leonardo_celery_email.Config'


LEONARDO_APPS = ['leonardo_celery_email', 'djcelery_email']

LEONARDO_CONFIG = {
    "CELERY_MAIL_FAIL_SILENTLY": (True, "Fail silently in sending emails")
}


class Config(AppConfig):
    name = 'leonardo_celery_email'
    verbose_name = "leonardo-celery-email"
