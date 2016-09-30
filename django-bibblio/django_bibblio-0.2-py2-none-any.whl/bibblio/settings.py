# -*- coding: utf-8 -*-
from django.conf import settings as site_settings
from django.core.exceptions import ImproperlyConfigured
import pytz


DEFAULT_SETTINGS = {
    'MINIMAL_RELEVANCE': 0.5,  # Only store items with a relevance of this or higher
    'CLIENT_ID': '',
    'CLIENT_SECRET': '',
    'DEFAULT_TIMEZONE': None,  # For naive datetimes, assume it is this time zone
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(site_settings, 'BIBBLIO_SETTINGS', {}))

if USER_SETTINGS['DEFAULT_TIMEZONE'] is None:
    USER_SETTINGS['DEFAULT_TIMEZONE'] = site_settings.TIME_ZONE

try:
    default_timezone = pytz.timezone(USER_SETTINGS['DEFAULT_TIMEZONE'])
except pytz.UnknownTimeZoneError as e:
    raise ImproperlyConfigured(str(e))

globals().update(USER_SETTINGS)
