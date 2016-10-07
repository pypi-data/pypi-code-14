
from mambo import register_package, get_config, abort, models, utils, cache
from mambo.core import get_installed_app_options
from mambo.exceptions import AppError

register_package(__package__)

__version__ = "1.0.0"

_app_id = None
_app_options = None
CACHE_TTL = 300

def main(**kw):
    global CACHE_TTL

    options = kw.get("options")
    CACHE_TTL = options.get("ttl", 300)


def _get_app_options():
    global _app_options
    if not _app_options:
        _app_options = get_installed_app_options(__name__)
    return _app_options


class MamboAppOptionCache(object):

    def set(self, key, value, description=None, app_id=None):
        cache.delete_memoized(self.get, key, app_id)
        models.MamboAppOption.set(key=key, value=value, description=description, app_id=app_id)

    @cache.memoize(CACHE_TTL)
    def get(self, key, app_id=None):
        return models.MamboAppOption.get_value(key, app_id=app_id)

    @classmethod
    def delete(cls, key, app_id=None):
        models.MamboAppOption.delete(key=key, app_id=app_id)
        cache.delete_memoized(self.get, key, app_id)

    @classmethod
    def clear_cache(cls):
        pass

cache_option = MamboAppOptionCache()

def set_app_id(id):
    """
    Set an app id
    :param id:
    :return:
    """
    global _app_id
    _app_id = id


def get(key, app_id=None):
    """
    Get an app config
    :param key:
    :param app_id:
    :return: mixed
    """
    if not app_id and _app_id:
        app_id = _app_id

    return cache_option.get(key, app_id=app_id)


def set(key, value, description=None, app_id=None):
    """
    Set an app config
    :param key:
    :param value:
    :param description:
    :param app_id:
    :return:
    """
    if not app_id and _app_id:
        app_id = _app_id
    cache_option.set(key=key,
                     value=value,
                     description=description,
                     app_id=app_id)


def delete(key, app_id):
    """
    Delete a key
    :param key:
    :param app_id:
    :return:
    """
    cache_option.delete(key, app_id=app_id)




