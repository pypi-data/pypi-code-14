from datetime import datetime, timedelta
import json
import requests

class DictObject(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__


class DynamicConfigSource(object):
    full_fetch_required = False

    def __init__(self):
        pass

    def get(self, key):
        raise Exception("You should be using a subclass of DynamicConfigSource.")

    def set(self, key, value):
        raise Exception("You should be using a subclass of DynamicConfigSource.")

    def get_all(self):
        raise Exception("You should be using a subclass of DynamicConfigSource")


class RedisConfigSource(DynamicConfigSource):
    def __init__(self, redis, prefix=None):
        super(RedisConfigSource, self).__init__()
        self.redis = redis
        self.prefix = prefix or "CONFIGI:"

    def _redis_key(self, key):
        return self.prefix + key

    def get(self, key):
        value = self.redis.get(self._redis_key(key))
        if value:
            return json.loads(value)
        return value

    def set(self, key, value):
        self.redis.set(self._redis_key(key), json.dumps(value))

    def delete(self, key):
        self.redis.delete(self._redis_key(key))

    def get_all(self):
        settings = {}
        for key in self.redis.scan_iter(self.prefix + "*"):
            settings[key.replace(self.prefix, "")] = json.loads(self.redis.get(key))
        return settings


class JSONConfigSource(DynamicConfigSource):
    full_fetch_required = True

    def __init__(self, url):
        super(JSONConfigSource, self).__init__()
        self.url = url

    def get(self, key):
        json_data = json.loads(requests.get(self.url))
        return json_data.get(key)

    def set(self, key, value):
        raise Exception("This source is read-only.")

    def delete(self, key):
        raise Exception("This source is read-only.")

    def get_all(self):
        return json.loads(requests.get(self.url))


class S3ConfigSource(DynamicConfigSource):
    full_fetch_required = True

    def __init__(self, s3_key_instance):
        super(S3ConfigSource, self).__init__()
        self.k = s3_key_instance

    def get(self, key):
        return self.get_all().get(key)

    def set(self, key, value):
        contents = self.get_all()
        contents[key] = value
        self.k.set_contents_from_string(json.dumps(contents))

    def delete(self, key):
        contents = self.get_all()
        del contents[key]
        self.k.set_contents_from_string(json.dumps(contents))

    def get_all(self):
        return json.loads(self.k.get_contents_as_string())


class DynamicConfig(object):
    intrinsic_keys = ['source', 'expiry', 'cache', 'quiet_mode', 'namespace_dicts', 'defaults']

    def __init__(self, source, expiry=300, quiet_mode=True, namespace_dicts=True, defaults=None):
        self.source = source
        self.expiry = expiry
        self.cache = {}
        self.quiet_mode = quiet_mode
        self.namespace_dicts = namespace_dicts
        self.defaults = defaults or {}

    def _is_expired(self, last_update):
        return (last_update + timedelta(seconds=self.expiry)) < datetime.utcnow()

    def _refresh(self, key):
        if self.source.full_fetch_required:
            self.cache = {k: (v, datetime.utcnow()) for k, v in self.source.get_all().items()}
        else:
            value = self.source.get(key)
            if value is not None:
                self.cache[key] = (value, datetime.utcnow())

        value = self.cache.get(key)
        if value is not None:
            return value[0]

        return value
    
    def all_values(self):
        return self.source.get_all()

    def delete(self, key):
        self.source.delete(key)

    def __getattr__(self, key):
        if key in DynamicConfig.intrinsic_keys:
            return super(DynamicConfig, self).__getattribute__(key)

        value = None

        try:
            data = self.cache.get(key)
            if data and not self._is_expired(data[1]):
                value = data[0]
            else:
                value = self._refresh(key)

        except Exception as e:
            import traceback
            traceback.print_exc()
            if self.quiet_mode:
                print "DynamicConfigError: Could not get key {}".format(key)
            else:
                raise DynamicConfigError("Could not get key {}".format(key))

        if value is None:
            value = self.defaults.get(key)

        if self.namespace_dicts and isinstance(value, dict):
            value = DictObject(value)

        return value

    def __setattr__(self, key, value):
        if key in DynamicConfig.intrinsic_keys:
            super(DynamicConfig, self).__setattr__(key, value)
            return
        try:
            self.cache[key] = (value, datetime.utcnow())
            self.source.set(key, value)
        except Exception as e:
            import traceback
            traceback.print_exc()
            if self.quiet_mode:
                print "DynamicConfigError: Could not set key {}".format(key)
                return
            else:
                raise DynamicConfigError("Could not set key {}".format(key))


class DynamicConfigError(Exception):
    pass

# End
