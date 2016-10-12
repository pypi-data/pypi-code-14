"""
AppData

A DB store to help save application data
Data will be shortly cached when accessed

"""


from mambo import register_package, get_config, abort, models, utils, cache
from mambo.core import get_installed_app_options
from mambo.exceptions import AppError

register_package(__package__)

__version__ = "1.0.0"

_app_options = None


def main(**kw): pass


def _get_app_options():
    global _app_options
    if not _app_options:
        _app_options = get_installed_app_options(__name__)
    return _app_options


def get_ttl():
    o = get_installed_app_options(__name__)
    return o.get("cache_ttl", 300)


@cache.memoize(get_ttl())
def _get_key(namespace, key):
    return AppData.get_data(namespace=namespace, key=key)


def _del_cache_key(namespace, key):
    cache.delete_memoized(_get_key, namespace, key)


class AppData(object):
    """
    Create an app data namespace to work with
    """
    def __init__(self, namespace):
        self.namespace = namespace
        self.db = models.AppData

    def set(self, key, value, description=None):
        k = self.db.get_by_key(namespace=self.namespace, key=key)
        if k:
            k.data = value
            _del_cache_key(namespace=self.namespace, key=key)
        else:
            self.db.new(namespace=self.namespace,
                        key=key,
                        value=value,
                        description=description)


    def get(self, key):
        return _get_key(namespace=self.namespace,
                        key=key)

    def delete(self, key):
        k = self.db.get_by_key(namespace=self.namespace, key=key)
        if k:
            k.delete()
        _del_cache_key(namespace=self.namespace, key=key)

    def has(self, key):
        return True \
            if self.db.get_by_key(namespace=self.namespace, key=key) \
            else False

    @classmethod
    def get_data(cls, namespace, key):
        d = models.AppData.get_by_key(namespace=namespace, key=key)
        return d.data

    @classmethod
    def clear_cache(cls):
        pass


