import django
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def detect_backend():
    try:
        # django-user-accounts
        import account
        if 'account' in settings.INSTALLED_APPS:
            return 'django-user-accounts'
    except ImportError:
        pass

    try:
        # allauth
        import allauth
        if 'allauth' in settings.INSTALLED_APPS:
            return 'allauth'
    except ImportError:
        pass

    # django-registration
    # no need... built on top of django.contrib.auth

    # django.contrib.auth
    # must be last because other extensions require it
    if 'django.contrib.auth' in settings.INSTALLED_APPS:
        if django.VERSION < (1, 9):
            raise ImproperlyConfigured('django.contrib.auth is only supported with Django >= 1.9')
        return 'contrib-auth'


class OpenCredSettings(object):
    @property
    def OPENCRED_AUTH_BACKEND(self):
        return getattr(settings, 'OPENCRED_AUTH_BACKEND', detect_backend())

    @property
    def OPENCRED_API_KEY(self):
        return getattr(settings, 'OPENCRED_API_KEY', None)

    @property
    def OPENCRED_EXEMPT_URLS(self):
        return getattr(settings, 'OPENCRED_EXEMPT_URLS', [])

    @property
    def OPENCRED_RESTRICT_MESSAGE(self):
        return getattr(settings, 'OPENCRED_RESTRICT_MESSAGE', 'Your password must be changed as it has been stolen.')

    @property
    def OPENCRED_RESTRICTED_GROUP(self):
        return getattr(settings, 'OPENCRED_RESTRICTED_GROUP', 'OpenCred detections')

    @property
    def OPENCRED_DISABLE_RESTRICTIONS(self):
        return getattr(settings, 'OPENCRED_DISABLE_RESTRICTIONS', False)


SETTINGS = OpenCredSettings()

ALLOWED_BACKENDS = ('contrib-auth', 'django-user-accounts', 'allauth')
if SETTINGS.OPENCRED_AUTH_BACKEND not in ALLOWED_BACKENDS:
    raise ImproperlyConfigured('Unable to detect authentication backend. ' +
                               'Try manually setting OPENCRED_AUTH_BACKEND to one of %s.' % (ALLOWED_BACKENDS,))

if not SETTINGS.OPENCRED_API_KEY:
    raise ImproperlyConfigured('OPENCRED_API_KEY is missing or empty.')
