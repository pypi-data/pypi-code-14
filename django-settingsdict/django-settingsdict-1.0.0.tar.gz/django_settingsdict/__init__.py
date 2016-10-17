from django.conf import settings
from django.test.signals import setting_changed
from django.utils.module_loading import import_string
from django.utils.functional import cached_property
from django.core.exceptions import ImproperlyConfigured

class SettingsDict(object):
    def __init__(self, name, defaults=None, required=None, removed=None, import_strings=None):
        self._name = name
        self._defaults = defaults or {}
        self._required = frozenset(required or ())
        self._removed = frozenset(removed or ())
        self._import_strings = frozenset(import_strings or ())

        self._listen_for_changes()

    @cached_property
    def _user_settings(self):
        """
        Resolve settings dict from django settings module.
        Validate that all the required keys are present and also that none of
        the removed keys do.
        Result is cached.
        """
        user_settings = getattr(settings, self._name, None)
        if not user_settings:
            raise ImproperlyConfigured("Settings file is missing dict options with name {}".format(self._name))
        keys = frozenset(user_settings.keys())

        required = self._required - keys
        if required:
            raise ImproperlyConfigured("Following options for {} are missing from settings file: {}".format(self._name, ', '.join(sorted(required))))

        removed = keys & self._removed
        if removed:
            raise ImproperlyConfigured("Following options for {} have been removed: {}".format(self._name, ', '.join(sorted(removed))))

        return user_settings

    def __getattr__(self, key):
        """
        Any attribute request that isn't known before (e.g. cached or
        defined in class) will be resolved as option.
        If value is not found from user provided settings default is used.
        If key is marked as import, value is imported using django.
        Result is cached.
        """
        if key not in self._defaults and key not in self._required:
            raise AttributeError("Invalid {} setting {}".format(self._name, key))

        try:
            val = self._user_settings[key]
        except KeyError:
            val = self._defaults[key]

        if val and key in self._import_strings:
            val = import_string(val)

        setattr(self, key, val)
        return val

    def _clear_cached(self):
        keep = set('_name', '_defaults', '_required', '_removed', '_import_strings')
        remove = set(self.__dict__.keys()) - keep
        for key in remove:
            del self.__dict__[key]

    def _listen_for_changes(self):
        def reload(*args, **kwargs):
            if kwargs['setting'] == self.name:
                self._clear_cached()
        setting_changed.connect(reload)
