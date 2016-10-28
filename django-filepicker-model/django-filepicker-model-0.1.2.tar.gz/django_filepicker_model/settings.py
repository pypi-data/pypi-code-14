import os

SECRET_KEY = '+++++++++++++++++++++++++++++++++++'

INSTALLED_APPS = [
    'django_filepicker_model'
]

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}