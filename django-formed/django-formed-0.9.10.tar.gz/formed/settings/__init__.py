# coding=utf-8
from django.conf import settings
from django.utils.translation import gettext as _

import defaults

# Constants

FORM_DEFINITION_ID_FIELD = 'form_definition_id'
FORM_DEFINITION_PAGE_FIELD = 'form_definition_page'
FORM_DEFINITION_PAGE_TYPE_FIELD = 'form_definition_page_type'

FORM_DEFINITION_PAGE_TYPE_PAGE = 'page'
FORM_DEFINITION_PAGE_TYPE_SUMMARY = 'summary'
FORM_DEFINITION_PAGE_TYPE_FINISH = 'finish'
FORM_DEFINITION_PAGE_TYPES = (
    FORM_DEFINITION_PAGE_TYPE_PAGE,
    FORM_DEFINITION_PAGE_TYPE_SUMMARY,
    FORM_DEFINITION_PAGE_TYPE_FINISH
)
FORMED_NAME_FIELD_REGEX = r'^[a-z]+[a-z0-9_\-]{0,}$'

# Settings

FORMED_SESSION_NAME = getattr(settings, 'FORMED_SESSION_NAME', 'formed')

FORMED_DEFINITION_DEFAULT_PAGE = getattr(settings, 'FORM_DEFINITION_DEFAULT_PAGE', 0)
FORMED_DEFINITION_DEFAULT_FIELD_TYPE = getattr(settings, 'FORM_DEFINITION_DEFAULT_FIELD_TYPE', 'CharField')

FORMED_NOTIFICATION_FROM_EMAIL = getattr(settings, 'FORMED_NOTIFICATION_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
FORMED_NOTIFICATION_DEFAULT_SUBJECT = getattr(settings, 'FORMED_NOTIFICATION_DEFAULT_SUBJECT',
                                              "Submission of form '{form_name}'")

# Whether or not to add a foreign key to the Site model
FORMED_USE_SITES_FRAMEWORK = getattr(settings, 'FORMED_USE_SITES_FRAMEWORK',
                                     'django.contrib.sites' in settings.INSTALLED_APPS)
# Admin settings:
FORMED_SHOW_JSON_FIELD = getattr(settings, 'FORMED_SHOW_JSON_FIELD', settings.DEBUG)
# Form settings:
FORMED_FORM_ERROR_CSS_CLASS = getattr(settings, 'FORMED_FORM_ERROR_CSS_CLASS', 'is-error')
FORMED_FORM_REQUIRED_CSS_CLASS = getattr(settings, 'FORMED_FORM_REQUIRED_CSS_CLASS', 'is-required')
FORMED_FORM_OPTIONAL_CSS_CLASS = getattr(settings, 'FORMED_FORM_OPTIONAL_CSS_CLASS', 'is-optional')

# The default form label suffix:
FORMED_FORM_LABEL_SUFFIX = getattr(settings, 'FORMED_FORM_LABEL_SUFFIX', '')
# The suffix applied when a field is required, set to None to disable:
FORMED_FORM_REQUIRED_LABEL_SUFFIX = getattr(settings, 'FORMED_FORM_REQUIRED_LABEL_SUFFIX', None)  # _(' (required)')
# The suffix applied when a field is optional, set to None to disable:
FORMED_FORM_OPTIONAL_LABEL_SUFFIX = getattr(settings, 'FORMED_FORM_OPTIONAL_LABEL_SUFFIX', _(' (optional)'))

# Modules to search for field types:
FORMED_FORM_FIELD_MODULES = getattr(settings, 'FORMED_FORM_FIELD_MODULES', defaults.FORMED_FORM_FIELD_MODULES)
FORMED_FORM_FIELD_MODULES.extend(getattr(settings, 'FORMED_ADDITIONAL_FORM_FIELD_MODULES', []))

# FORMED_DEFAULT_CUSTOM_FIELDS = [
#     form_fields.FirstNameField,
#     form_fields.LastNamePrefixField,
#     form_fields.LastNameField,
#     form_fields.NameField
# ]
# FORMED_CUSTOM_FIELDS = getattr(settings, 'FORMED_CUSTOM_FIELDS', FORMED_DEFAULT_CUSTOM_FIELDS)

# Default prototype of a form field
FORMED_FORM_FIELD = getattr(settings, 'FORMED_FORM_FIELD', defaults.FORMED_FORM_FIELD)

# Available form fields:
FORMED_FORM_FIELDS = getattr(settings, 'FORMED_FORM_FIELDS', defaults.FORMED_FORM_FIELDS)
FORMED_FORM_FIELDS.update(getattr(settings, 'FORMED_ADDITIONAL_FORM_FIELDS', {}))

# Categorisation of the list of input types
FORMED_FORM_FIELD_CATEGORIES = getattr(settings, 'FORMED_FORM_FIELD_CATEGORIES', defaults.FORMED_FORM_FIELD_CATEGORIES)

# Path to function that returns a 'source url' from the given django.http.HttpRequest object
FORMED_SOURCE_URL_PROVIDER = getattr(settings, 'FORMED_SOURCE_URL_PROVIDER', 'formed.utils.get_source_url_from_request')
