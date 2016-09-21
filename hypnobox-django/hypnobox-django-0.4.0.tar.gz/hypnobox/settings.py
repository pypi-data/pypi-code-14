# coding: utf-8

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .specs import SPECS


SPEC_VERSION = getattr(settings, 'HYPNOBOX_SPEC_VERSION', max(SPECS))
DOMAIN = getattr(settings, 'HYPNOBOX_DOMAIN', 'hypnobox.com.br')
CLIENT_ID = getattr(settings, 'HYPNOBOX_CLIENT_ID', 'demo')

if SPEC_VERSION not in SPECS:
    raise ImproperlyConfigured(
        'Hypnobox spec version not supported: {}.'.format(SPEC_VERSION))
