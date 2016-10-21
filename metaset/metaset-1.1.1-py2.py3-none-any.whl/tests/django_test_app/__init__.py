# -*- coding: utf-8 -*-
from django.apps import apps
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'metaset_test',
            }
        },
        INSTALLED_APPS=[
            'tests.django_test_app',
        ],
    )
apps.populate(settings.INSTALLED_APPS)
