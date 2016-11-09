"""
Django settings for our farmdrop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from datetime import date
import os
import sys
gettext = lambda s: s

from configurations import Configuration, values
from django.contrib.messages import constants as messages


class Common(Configuration):
    # You'll likely want to add your own auth model.
    ADMINS =  (
        ('Colin Powell', 'colin.powell@gmail.com'),
    )
    MANAGERS = ADMINS

    SSL = False

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(BASE_DIR, 'farmdrop/apps'))
    sys.path.insert(0, os.path.join(BASE_DIR, 'farmdrop/frozen_deps'))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['.farmdrop.org']

    PUBLIC_ROOT = values.Value(os.path.join(BASE_DIR, 'public'))
    STATIC_ROOT = os.path.join(PUBLIC_ROOT.setup('PUBLIC_ROOT'), 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "farmdrop/static"),
    )

    MEDIA_ROOT = values.Value(PUBLIC_ROOT.setup('PUBLIC_ROOT'), 'media')
    MEDIA_URL = "/media/"
    ADMIN_MEDIA_PREFIX = "/static/admin/"

    AWS_ACCESS_KEY_ID=values.Value('')
    AWS_SECRET_ACCESS_KEY=values.Value('')
    AWS_HEADERS = {'ExpiresDefault': 'access plus 30 days',
                   'Cache-Control': 'max-age=86400', }

    DEFAULT_BUCKET_PATH = values.Value("farmdrop-media")
    AWS_DEFAULT_DOMAIN = ""
    AWS_STORAGE_BUCKET_NAME = DEFAULT_BUCKET_PATH

    # Settings for Amazon SQS connection
    BROKER_TRANSPORT = values.Value()
    BROKER_TRANSPORT_OPTIONS = { 'region': 'us-east-1', }
    if BROKER_TRANSPORT == 'sqs':
        import urllib
        BROKER_USER = urllib.parse.quote(AWS_ACCESS_KEY_ID.setup('AWS_ACCESS_KEY_ID'))
        BROKER_PASSWORD = urllib.parse.quote(AWS_SECRET_ACCESS_KEY.setup('AWS_SECRET_ACCESS_KEY'))
    else:
        BROKER_URL = values.Value('amqp://guest:guest@localhost:5672/')
        BROKER_USER = values.Value()
        BROKER_PASSWORD = values.Value()

    from oscar import get_core_apps
    # Application definition
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.admin',
        'django.contrib.staticfiles',
        'django.contrib.redirects',
        'django.contrib.sitemaps',
        'django.contrib.flatpages',

        'rest_framework',
        'corsheaders',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.twitter',
        'django_extensions',
        'robots',
        'floppyforms',
        'django_nose',
        'typogrify',
        'easy_thumbnails',
        'django_jenkins',

        #'compressor',
        'widget_tweaks',
    ] + get_core_apps()

    if AWS_ACCESS_KEY_ID.setup('AWS_ACCESS_KEY_ID'):
        INSTALLED_APPS = Common.INSTALLED_APPS + ('storages',)
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'


    PROJECT_APPS = ()

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

    AUTHENTICATION_BACKENDS = (
        'oscar.apps.customer.auth_backends.EmailBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    LOGIN_URL = '/account/login'

    DEFAULT_CURRENCY = 'USD'
    AVAILABLE_CURRENCIES = [DEFAULT_CURRENCY]
    DEFAULT_WEIGHT = 'lb'

    ACCOUNT_ACTIVATION_DAYS = 3

    LOGIN_REDIRECT_URL = 'home'

    FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')

    GOOGLE_ANALYTICS_TRACKING_ID = os.environ.get('GOOGLE_ANALYTICS_TRACKING_ID')
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    from oscar.defaults import (OSCAR_REQUIRED_ADDRESS_FIELDS, OSCAR_SLUG_ALLOW_UNICODE,
                                OSCAR_IMAGE_FOLDER, OSCAR_MODERATE_REVIEWS, OSCAR_PROMOTION_FOLDER,
                                OSCAR_DELETE_IMAGE_FILES, OSCAR_EAGER_ALERTS, OSCAR_REVIEWS_PER_PAGE,
                                OSCAR_SEARCH_FACETS, OSCAR_PRODUCTS_PER_PAGE, OSCAR_OFFERS_PER_PAGE,
                                OSCAR_ACCOUNTS_REDIRECT_URL, OSCAR_HOMEPAGE, OSCAR_EMAILS_PER_PAGE,
                                OSCAR_ORDERS_PER_PAGE, OSCAR_ADDRESSES_PER_PAGE, OSCAR_NOTIFICATIONS_PER_PAGE,
                                OSCAR_DASHBOARD_ITEMS_PER_PAGE, OSCAR_STOCK_ALERTS_PER_PAGE,
                                OSCAR_PROMOTION_POSITIONS, OSCAR_HIDDEN_FEATURES, OSCAR_ALLOW_ANON_CHECKOUT,
                                OSCAR_PROMOTIONS_ENABLED, OSCAR_SHOP_NAME, OSCAR_SHOP_TAGLINE,
                                OSCAR_BASKET_COOKIE_OPEN, OSCAR_DEFAULT_CURRENCY, OSCAR_SLUG_MAP,
                                OSCAR_DASHBOARD_NAVIGATION, OSCAR_DASHBOARD_DEFAULT_ACCESS_FUNCTION,
                                OSCAR_SLUG_BLACKLIST, OSCAR_COOKIES_DELETE_ON_LOGOUT,
                                OSCAR_PRODUCT_SEARCH_HANDLER)
    OSCAR_SHOP_NAME=os.environ.get('SHOP_NAME', 'Farmdrop')

    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

    CHECKOUT_PAYMENT_CHOICES = [
        ('default', 'Dummy provider')
    ]

    MESSAGE_TAGS = {
        messages.ERROR: 'danger',
    }

    LOW_STOCK_THRESHOLD = 10

    PAGINATE_BY = 16

    TEST_RUNNER = ''

    from oscar import OSCAR_MAIN_TEMPLATE_DIR

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                os.path.join(BASE_DIR, 'farmdrop/templates'),
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',

                    'oscar.apps.search.context_processors.search_form',
                    'oscar.apps.promotions.context_processors.promotions',
                    'oscar.apps.checkout.context_processors.checkout',
                    'oscar.apps.customer.notifications.context_processors.notifications',
                    'oscar.core.context_processors.metadata'],
	            'string_if_invalid': '<< MISSING VARIABLE "%s" >>' if DEBUG else ''
            },
        },
    ]

    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'oscar.apps.basket.middleware.BasketMiddleware',
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ]

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    ACCOUNT_AUTHENTICATION_METHOD = "email"
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_USERNAME_REQUIRED = False

    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",)

    ROOT_URLCONF = 'farmdrop.urls'

    WSGI_APPLICATION = 'farmdrop.wsgi.application'

    NEVERCACHE_KEY = values.Value('klladsf-wefkjlwef-wekjlwef--wefjlkjfslkxvl')
    SCC_CUSTOM_URL_CACHE = ()

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/
    TIME_ZONE = 'America/New_York'
    LANGUAGE_CODE = 'en-us'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    SITE_ID = 1

    ALLOWED_HOSTS = values.Value('*')

    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

    PROJECT_DIRNAME = BASE_DIR.split(os.sep)[-1]

    CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

    # Account activations automatically expire after this period
    ACCOUNT_ACTIVATION_DAYS = 14

    LOGIN_EXEMPT_URLS = ['', '/',
                         '/accounts/login/',
                         'login',
                         '/accounts/signup/']

    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_URL = '/accounts/logout/'

    #HAYSTACK_ROUTERS = ['aldryn_search.router.LanguageRouter',]
    HAYSTACK_URL = values.Value('whoosh:{0}/whoosh_index'.format(BASE_DIR))

    import dj_haystack_url
    HAYSTACK_CONNECTIONS = {'default': dj_haystack_url.parse(HAYSTACK_URL.setup('HAYSTACK_URL')) }

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOG_LEVEL = os.getenv('DJANGO_LOG_LEVEL', 'INFO')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                '%(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
                'formatter': 'simple'
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True
            },
        }
    }

class Dev(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    DATABASES = values.DatabaseURLValue('sqlite:///{0}'.format(
        os.path.join(Common.BASE_DIR, 'db.sqlite3'),
        environ=True))

    SECRET_KEY = 'notasecretatall'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INSTALLED_APPS = Common.INSTALLED_APPS + ['debug_toolbar',]
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + [
        'debug_toolbar.middleware.DebugToolbarMiddleware',]


class Stage(Common):
    DEBUG = True

    SECRET_KEY = values.SecretValue()

    SSL = True

    EMAIL_HOST = values.Value('localhost')
    EMAIL_HOST_USER = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_PORT = values.Value()
    EMAIL_USE_TLS = values.BooleanValue(False)

    CACHES = values.CacheURLValue('memcached://127.0.0.1:11211')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    Common.LOGGING['handlers']['sentry'] = { 'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler', }
    Common.LOGGING['loggers'] = {
            '': {
                'handlers': ['sentry'],
                'level': Common.LOG_LEVEL,
                'propagate': True,
            }
    }


class Prod(Common):
    """
    The in-production settings.
    """
    DEBUG = False

    SECRET_KEY = values.SecretValue()

    SSL = True

    EMAIL_HOST = values.Value()
    EMAIL_HOST_USER = values.Value()
    EMAIL_HOST_PASSWORD = values.Value()
    EMAIL_PORT = values.Value()
    EMAIL_USE_TLS = values.BooleanValue(True)

    CACHES = values.CacheURLValue('memcached://127.0.0.1:11211')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + [
        'smart_cache_control.middleware.SmartCacheControlMiddleware',]

    Common.LOGGING['handlers']['sentry'] = {
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
    }
    Common.LOGGING['loggers'] = {
        'django.request': {
            'handlers': ['sentry'],
            'level': 'WARNING',
            'propagate': True,
        },
    }

    DSN_VALUE = values.Value()

    # If we're on production, connect to Sentry
    RAVEN_CONFIG = {
        'dsn': DSN_VALUE.setup('DSN_VALUE'),
    }

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'raven.contrib.django.raven_compat',]
