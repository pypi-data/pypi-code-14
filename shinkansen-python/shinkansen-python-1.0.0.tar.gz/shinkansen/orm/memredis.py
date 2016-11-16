import logging

log = logging.getLogger(__name__)


class Error(Exception):
    pass


class Pipeline(object):
    def __init__(self, memredis):
        self._memredis = memredis
        self._results = []

    def __enter__(self):
        return self

    def __exit__(self, *a, **k):
        pass

    def execute(self):
        return self._results

    def _decorator(self, func):
        def wrapper(*a, **k):
            try:
                result = func(*a, **k)
            except Error, e:
                result = e
            self._results.append(result)
            return self
        return wrapper

    def __getattr__(self, name):
        if not hasattr(self._memredis, name):
            raise TypeError('No attribute %s' % (name,))
        return self._decorator(getattr(self._memredis, name))


class KeyTypes(object):
    HASH = 'hash'
    SET = 'set'


# This version of MemRedis would work if multiprocessing supported dynamically allocated shared resources.
# Unfortunately it requires that all shared resources be inherited from the parent process.
# class MemRedis(object):
#     _manager = None
#     _data = None

#     @classmethod
#     def init(cls, manager):
#         if cls._manager is not None:
#             raise Error('%s is already initialized' % (cls.__name__,))
#         cls._manager = manager
#         cls._data = cls._manager.dict()
#         cls._datatypes = cls._manager.dict()

#     def __init__(self):
#         if self.__class__._manager is None:
#             raise Error('You must call %(cls)s.init before instantiating %(cls)s' % {
#                 'cls': self.__class__.__name__
#             })

#     def pipeline(self):
#         return Pipeline(self)

#     def exists(self, key):
#         return key in self._data

#     def delete(self, *keys):
#         numdel = 0
#         for key in keys:
#             if key not in self._data:
#                 continue
#             del self._data[key]
#             del self._datatypes[key]
#             numdel += 1
#         return numdel

#     def sadd(self, key, *values):
#         if key not in self._data:
#             self._data[key] = self._manager.dict()
#             self._datatypes[key] = KeyTypes.SET
#         elif self._datatypes[key] != KeyTypes.SET:
#             raise Error('key %s is type %s, not set' % (key, self._datatypes[key]))
#         _set = self._data[key]
#         numadded = 0
#         for value in values:
#             if value in _set:
#                 continue
#             _set[value] = True
#             numadded += 1
#         return numadded

#     def srem(self, key, *values):
#         if key not in self._data:
#             return 0
#         if self._datatypes[key] != KeyTypes.SET:
#             raise Error('key %s is type %s, not set' % (key, self._datatypes[key]))
#         _set = self._data[key]
#         numremoved = 0
#         for value in values:
#             if value not in _set:
#                 continue
#             del _set[value]
#             numremoved += 1
#         return numremoved

#     def smove(self, from_key, to_key, value):
#         if self.srem(from_key, value) > 0:
#             self.sadd(to_key, value)
#             return 1
#         return 0

#     def smembers(self, key):
#         if key not in self._data:
#             return set()
#         if self._datatypes[key] != KeyTypes.SET:
#             raise Error('key %s is type %s, not set' % (key, self._datatypes[key]))
#         return set(self._data[key].keys())

#     def hmset(self, key, mapping):
#         if key not in self._data:
#             self._data[key] = self._manager.dict()
#             self._datatypes[key] = KeyTypes.HASH
#         elif self._datatypes[key] != KeyTypes.HASH:
#             raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
#         _hash = self._data[key]
#         for key, value in mapping.iteritems():
#             _hash[key] = value
#         return True

#     def hmget(self, key, fields):
#         if key not in self._data:
#             return [None] * len(fields)
#         if self._datatypes[key] != KeyTypes.HASH:
#             raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
#         result = []
#         _hash = self._data[key]
#         for field in fields:
#             result.append(_hash.get(field))
#         return result

#     def hgetall(self, key):
#         if key not in self._data:
#             return {}
#         if self._datatypes[key] != KeyTypes.HASH:
#             raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
#         return dict(self._data[key])

#     def hdel(self, key, *fields):
#         if key not in self._data:
#             return 0
#         if self._datatypes[key] != KeyTypes.HASH:
#             raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
#         numdeleted = 0
#         _hash = self._data[key]
#         for field in fields:
#             if field not in _hash:
#                 continue
#             del _hash[field]
#             numdeleted += 1
#         return numdeleted

class MemRedis(object):
    _manager = None
    _data = None

    @classmethod
    def init(cls, manager):
        if cls._manager is not None:
            raise Error('%s is already initialized' % (cls.__name__,))
        cls._manager = manager
        cls._data = cls._manager.dict()
        cls._datatypes = cls._manager.dict()

    def __init__(self):
        if self.__class__._manager is None:
            raise Error('You must call %(cls)s.init before instantiating %(cls)s' % {
                'cls': self.__class__.__name__
            })

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def pipeline(self):
        return Pipeline(self)

    def exists(self, key):
        log.debug('MemRedis.exists(%r)', key)
        return key in self._data

    def delete(self, *keys):
        log.debug('MemRedis.delete(*%r)', keys)
        numdel = 0
        for key in keys:
            if key not in self._data:
                continue
            del self._data[key]
            del self._datatypes[key]
            numdel += 1
        return numdel

    def sadd(self, key, *values):
        log.debug('MemRedis.sadd(%r, *%r)', key, values)
        if key not in self._data:
            self._data[key] = set()
            self._datatypes[key] = KeyTypes.SET
        elif self._datatypes[key] != KeyTypes.SET:
            raise Error('key %s is type %s, not set' % (key, self._datatypes[key]))
        _set = self._data[key]
        numadded = 0
        for value in values:
            if value in _set:
                continue
            _set.add(value)
            numadded += 1
        # set back to the managed dict so it picks up the changes
        self._data[key] = _set
        return numadded

    def srem(self, key, *values):
        log.debug('MemRedis.srem(%r, *%r)', key, values)
        if key not in self._data:
            return 0
        if self._datatypes[key] != KeyTypes.SET:
            raise Error('key %s is type %s, not set' % (key, self._datatypes[key]))
        _set = self._data[key]
        numremoved = 0
        for value in values:
            if value not in _set:
                continue
            _set.remove(value)
            numremoved += 1
        # set back to the managed dict so it picks up the changes
        self._data[key] = _set
        return numremoved

    def smove(self, from_key, to_key, value):
        log.debug('MemRedis.smove(%r, %r, %r)', from_key, to_key, value)
        if self.srem(from_key, value) > 0:
            self.sadd(to_key, value)
            return 1
        return 0

    def smembers(self, key):
        log.debug('MemRedis.smembers(%r)', key)
        if key not in self._data:
            return set()
        if self._datatypes[key] != KeyTypes.SET:
            raise Error('key %s is type %s, not set' % (key, self._datatypes[key]))
        return set(self._data[key])

    def hmset(self, key, mapping):
        log.debug('MemRedis.hmset(%r, %r)', key, mapping)
        if key not in self._data:
            log.debug('  Creating record %r', key)
            self._data[key] = {}
            self._datatypes[key] = KeyTypes.HASH
        elif self._datatypes[key] != KeyTypes.HASH:
            raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
        _hash = self._data[key]
        for _key, value in mapping.iteritems():
            _hash[_key] = value
        # set back to the managed dict so it picks up the changes
        self._data[key] = _hash
        return True

    def hdel(self, key, *fields):
        log.debug('MemRedis.hdel(%r, *%r)', key, fields)
        if key not in self._data:
            return 0
        if self._datatypes[key] != KeyTypes.HASH:
            raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
        numdeleted = 0
        _hash = self._data[key]
        for field in fields:
            if field not in _hash:
                continue
            del _hash[field]
            numdeleted += 1
        # set back to the managed dict so it picks up the changes
        self._data[key] = _hash
        return numdeleted

    def hmget(self, key, fields):
        log.debug('MemRedis.hmget(%r, %r)', key, fields)
        if key not in self._data:
            return [None] * len(fields)
        if self._datatypes[key] != KeyTypes.HASH:
            raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
        result = []
        _hash = self._data[key]
        for field in fields:
            result.append(_hash.get(field))
        return result

    def hgetall(self, key):
        log.debug('MemRedis.hgetall(%r)', key)
        if key not in self._data:
            return {}
        if self._datatypes[key] != KeyTypes.HASH:
            raise Error('key %s is type %s, not hash' % (key, self._datatypes[key]))
        return dict(self._data[key])
