
from django.conf import settings
from djcelery_email.backends import CeleryEmailBackend


class FailSilentlyEmailBackend(CeleryEmailBackend):

    def __init__(self, *args, **kwargs):
        super(FailSilentlyEmailBackend, self).__init__(
            settings.CELERY_MAIL_FAIL_SILENTLY)
