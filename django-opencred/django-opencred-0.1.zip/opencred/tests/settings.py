try:
    import account
except ImportError:
    account = None

try:
    import allauth
except ImportError:
    allauth = None

import os

import django

DEBUG = False

LANGUAGES = (
    ('en', 'English'),
)

LANGUAGE_CODE = 'en'

USE_TZ = False
USE_I18N = True

SECRET_KEY = 'not-really'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
    },
}

ROOT_URLCONF = 'opencred.tests.urls'

SITE_ID = 1

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

NO_NEW_STYLE_MIDDLEWARE = False

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'opencred.password_validation.OpenCredValidator',
    },
]

if account:
    # django-user-accounts
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'account',
        'opencred',
    ]

    NO_NEW_STYLE_MIDDLEWARE = True
    _MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'account.middleware.LocaleMiddleware',
        'account.middleware.TimezoneMiddleware',
        'opencred.middleware.OpenCredMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'account.context_processors.account',
        'django.contrib.messages.context_processors.messages',
    )
elif allauth:
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'allauth',
        'allauth.account',
        'opencred',
    )

    _MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'opencred.middleware.OpenCredMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.messages.context_processors.messages',
    )
else:
    # django.contrib.auth
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'opencred',
    ]

    _MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'opencred.middleware.OpenCredMiddleware',
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    )

NO_NEW_STYLE_MIDDLEWARE = NO_NEW_STYLE_MIDDLEWARE or django.VERSION < (1, 10)

if not NO_NEW_STYLE_MIDDLEWARE:
    MIDDLEWARE = _MIDDLEWARE
else:
    MIDDLEWARE_CLASSES = _MIDDLEWARE

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS
        },
    },
]

OPENCRED_API_KEY = 'hello'
