"""
This projects settings.
"""
# These settings can be imported with the django_app_importer tool
import os

URLCONF = 'urls'
DEFAULT_SERVER = os.environ.get('CENVARS_URL', 'https://localhost:8000')
RSA_KEYSIZE = 2048

CENVARS_KEY = os.environ.get('CENVARS_KEY')

CENVARS_DATABASE = 'cenvars'

DATABASES = {
    CENVARS_DATABASE: {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'file::memory:?cache=shared'}
}

# pylint:disable=wrong-import-position
import django_integrator
django_integrator.add_application('django_memdb')
