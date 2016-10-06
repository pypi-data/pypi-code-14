from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from autotranslate.conf import settings as autotranslate_settings
import hashlib
import time
import six
import django


try:
    from django.core.cache import caches
    cache = caches[autotranslate_settings.AUTOTRANSLATE_CACHE_NAME]
except ImportError:
    from django.core.cache import get_cache
    cache = get_cache(autotranslate_settings.AUTOTRANSLATE_CACHE_NAME)

try:
    import importlib
except ImportError:
    from django.utils import importlib


class BaseAutotranslateStorage(object):
    def __init__(self, request):
        self.request = request

    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, val):
        raise NotImplementedError

    def has(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError


class DummyAutotranslateStorage(BaseAutotranslateStorage):
    def get(self, key, default=None):
        return default

    def set(self, key, val):
        pass

    def has(self, key):
        return False

    def delete(self, key):
        pass


class SessionAutotranslateStorage(BaseAutotranslateStorage):
    def __init__(self, request):
        super(SessionAutotranslateStorage, self).__init__(request)

        if 'signed_cookies' in settings.SESSION_ENGINE and django.VERSION[1] >= 6 and 'pickle' not in settings.SESSION_SERIALIZER.lower():
            raise ImproperlyConfigured("Sorry, but dj-translate doesn't support the `signed_cookies` SESSION_ENGINE in Django >= 1.6, because autotranslate specific session files cannot be serialized.")

    def get(self, key, default=None):
        if key in self.request.session:
            return self.request.session[key]
        return default

    def set(self, key, val):
        self.request.session[key] = val

    def has(self, key):
        return key in self.request.session

    def delete(self, key):
        del(self.request.session[key])


class CacheAutotranslateStorage(BaseAutotranslateStorage):
    # unlike the session storage backend, cache is shared among all users
    # so we need to per-user key prefix, which we store in the session
    def __init__(self, request):
        super(CacheAutotranslateStorage, self).__init__(request)

        if 'autotranslate_cache_storage_key_prefix' in self.request.session:
            self._key_prefix = self.request.session['autotranslate_cache_storage_key_prefix']
        else:
            self._key_prefix = hashlib.new('sha1', six.text_type(time.time()).encode('utf8')).hexdigest()
            self.request.session['autotranslate_cache_storage_key_prefix'] = self._key_prefix

        if self.request.session['autotranslate_cache_storage_key_prefix'] != self._key_prefix:
            raise ImproperlyConfigured("You can't use the CacheAutotranslateStorage because your Django Session storage doesn't seem to be working. The CacheAutotranslateStorage relies on the Django Session storage to avoid conflicts.")

        # Make sure we're not using DummyCache
        if 'dummycache' in settings.CACHES[autotranslate_settings.AUTOTRANSLATE_CACHE_NAME]['BACKEND'].lower():
            raise ImproperlyConfigured("You can't use the CacheAutotranslateStorage if your cache isn't correctly set up (you are using the DummyCache cache backend).")

        # Make sure the cache actually works
        try:
            self.set('autotranslate_cache_test', 'autotranslate')
            if not self.get('autotranslate_cache_test') == 'autotranslate':
                raise ImproperlyConfigured("You can't use the CacheAutotranslateStorage if your cache isn't correctly set up, please double check your Django DATABASES setting and that the cache server is responding.")
        finally:
            self.delete('autotranslate_cache_test')

    def get(self, key, default=None):
        #print ('get', self._key_prefix + key)
        return cache.get(self._key_prefix + key, default)

    def set(self, key, val):
        #print ('set', self._key_prefix + key)
        cache.set(self._key_prefix + key, val, 86400)

    def has(self, key):
        #print ('has', self._key_prefix + key)
        return (self._key_prefix + key) in cache

    def delete(self, key):
        #print ('del', self._key_prefix + key)
        cache.delete(self._key_prefix + key)


def get_storage(request):
    from autotranslate.conf import settings
    storage_module, storage_class = settings.STORAGE_CLASS.rsplit('.', 1)
    storage_module = importlib.import_module(storage_module)
    return getattr(storage_module, storage_class)(request)
