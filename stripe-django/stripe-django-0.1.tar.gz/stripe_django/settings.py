# -*- coding: utf-8 -*-

SECRET_KEY = 'test'

INSTALLED_APPS = [
    'stripe_django'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
