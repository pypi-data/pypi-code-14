# -*- coding:utf-8 -*-
import importlib

from flask._compat import string_types


def _gettext(s):
    return s

DEFAULTS = {
    'GETTEXT_FUNC': _gettext,
    'AUTHENTICATION_CLASSES': (),
    'PERMISSION_CLASSES': (
        'palmer.permissions.AllowAny',
    ),
    'RENDERER_CLASS': 'palmer.renderers.JSONRenderer'
}


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        # Nod to tastypie's use of importlib.
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except ImportError as exc:
        format_ = "Could not import '%s' for API setting '%s'. %s."
        msg = format_ % (val, setting_name, exc)
        raise ImportError(msg)


def perform_imports(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if isinstance(val, string_types):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [perform_imports(item, setting_name) for item in val]
    return val


class APIConfig(object):
    def __init__(self, user_config=None):
        self.user_config = user_config or {}

    def get_or_default(self, name):
        default = DEFAULTS[name]
        val = self.user_config.get(name, default)
        return perform_imports(val, name)

    @property
    def GETTEXT_FUNC(self):
        default = DEFAULTS['GETTEXT_FUNC']
        val = self.user_config.get('GETTEXT_FUNC', default)
        return val if callable(val) else perform_imports(val, 'GETTEXT_FUNC')

    @property
    def AUTHENTICATION_CLASSES(self):
        return self.get_or_default('AUTHENTICATION_CLASSES')

    @property
    def PERMISSION_CLASSES(self):
        return self.get_or_default('PERMISSION_CLASSES')

    @property
    def RENDERER_CLASS(self):
        return self.get_or_default('RENDERER_CLASS')

default_config = APIConfig()
