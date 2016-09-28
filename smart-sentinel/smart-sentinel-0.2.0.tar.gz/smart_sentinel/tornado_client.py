#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smart-sentinel.
# https://github.com/rfloriano/smart-sentinel

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Rafael Floriano da Silva <rflorianobr@gmail.com>
import functools

import tornado.gen
import redis
from redis.exceptions import ConnectionError, TimeoutError, ReadOnlyError

from smart_sentinel.client import SmartSentinel


class BaseTornadoSmartSentinel(object):
    def __delitem__(self, *args, **kwargs):
        raise NotImplementedError(
            'del sentinel_instance[key], is not supported for coroutines '
            'you should to use yield sentinel_instance.delete(key)'
        )

    def __setitem__(self, *args, **kwargs):
        raise NotImplementedError(
            'sentinel_instance[key] = value, is not supported for coroutines '
            'you should to use yield sentinel_instance.set(key, value)'
        )

    def __getitem__(self, *args, **kwargs):
        raise NotImplementedError(
            'sentinel_instance[key], is not supported for coroutines '
            'you should to use yield sentinel_instance.get(key)'
        )


class TornadoStrictRedis(BaseTornadoSmartSentinel):
    def __init__(self, *args, **kwargs):
        self._redis = redis.StrictRedis(*args, **kwargs)

    def __getattr__(self, attr):
        method = getattr(self._redis, attr)
        return functools.partial(self._exec, method)

    def __dir__(self):
        return dir(self._redis)

    @tornado.gen.coroutine
    def _exec(self, method, *args, **kwargs):
        result = yield tornado.gen.Task(self._exec_adapter, method, *args, **kwargs)
        raise tornado.gen.Return(result)

    def _exec_adapter(self, method, *args, **kwargs):
        callback = kwargs.pop('callback', None)
        # import ipdb; ipdb.set_trace()
        result = method(*args, **kwargs)
        return callback(result)


class TornadoSmartSentinel(BaseTornadoSmartSentinel, SmartSentinel):
    def __delitem__(self, *args, **kwargs):
        raise NotImplementedError(
            'del sentinel_instance[key], is not supported for coroutines '
            'you should to use yield sentinel_instance.delete(key)'
        )

    def __setitem__(self, *args, **kwargs):
        raise NotImplementedError(
            'sentinel_instance[key] = value, is not supported for coroutines '
            'you should to use yield sentinel_instance.set(key, value)'
        )

    def __getitem__(self, *args, **kwargs):
        raise NotImplementedError(
            'sentinel_instance[key], is not supported for coroutines '
            'you should to use yield sentinel_instance.get(key)'
        )

    @tornado.gen.coroutine
    def _exec(self, method, *args, **kwargs):
        try:
            result = yield tornado.gen.Task(self._exec_adapter, method, *args, **kwargs)
        except (ConnectionError, TimeoutError, ReadOnlyError):
            type_ = self._get_operation_type(method.__name__)
            if type_ == 'master':
                self._master = self._get_master()
                method = getattr(self._master, method.__name__)
            else:
                self._slave = self._get_slave()
                method = getattr(self._slave, method.__name__)
            result = yield tornado.gen.Task(self._exec_adapter, method, *args, **kwargs)
        raise tornado.gen.Return(result)

    def _exec_adapter(self, method, *args, **kwargs):
        callback = kwargs.pop('callback', None)
        result = method(*args, **kwargs)
        return callback(result)
