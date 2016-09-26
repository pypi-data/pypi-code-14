#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of smart-sentinel.
# https://github.com/rfloriano/smart-sentinel

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2016, Rafael Floriano da Silva <rflorianobr@gmail.com>

import functools

import redis.sentinel
from redis.exceptions import ConnectionError, TimeoutError, ReadOnlyError


class SmartSentinel(object):
    def __init__(self, master_name, *args, **kwargs):
        self._socket_timeout = kwargs.get('socket_timeout', None)
        self._sentinel = redis.sentinel.Sentinel(*args, **kwargs)
        self._master_name = master_name
        self._master = self._get_master()
        self._slave = self._get_slave()

    def _get_master(self):
        return self._sentinel.master_for(
            self._master_name,
            socket_timeout=self._socket_timeout,
            retry_on_timeout=True
        )

    def _get_slave(self):
        return self._sentinel.slave_for(
            self._master_name,
            socket_timeout=self._socket_timeout,
            retry_on_timeout=True
        )

    def _get_operation_type(self, attr):
        return 'master' if attr in self._get_write_operations() else 'slave'

    def __getattr__(self, attr):
        type_ = self._get_operation_type(attr)
        if type_ == 'master':
            method = getattr(self._master, attr)
        else:
            method = getattr(self._slave, attr)
        return functools.partial(self._exec, method)

    def __delitem__(self, *args, **kwargs):
        method = self.__getattr__('__delitem__')
        return method(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        method = self.__getattr__('__setitem__')
        return method(*args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        method = self.__getattr__('__getitem__')
        return method(*args, **kwargs)

    def __dir__(self):
        return dir(self._master)

    def _exec(self, method, *args, **kwargs):
        try:
            return method(*args, **kwargs)
        except (ConnectionError, TimeoutError, ReadOnlyError):
            type_ = self._get_operation_type(method.__name__)
            if type_ == 'master':
                self._master = self._get_master()
                method = getattr(self._master, method.__name__)
            else:
                self._slave = self._get_slave()
                method = getattr(self._slave, method.__name__)
        return method(*args, **kwargs)

    def _get_write_operations(self):
        return [
            'append',
            'bitop',
            'decr',
            'delete',
            '__delitem__',
            'expire',
            'expireat',
            'getset',
            'incr',
            'incrby',
            'incrbyfloat',
            'mset',
            'msetnx',
            'move',
            'persist',
            'pexpire',
            'pexpireat',
            'psetex',
            'rename',
            'renamenx',
            'restore',
            'set',
            '__setitem__',
            'setbit',
            'setex',
            'setnx',
            'setrange',
            'ttl',
            'type',
            'watch',
            'unwatch',
            'blpop',
            'brpop',
            'brpoplpush',
            'lindex',
            'lpop',
            'lpush',
            'lpushx',
            'lrem',
            'lset',
            'ltrim',
            'rpop',
            'rpoplpush',
            'rpush',
            'rpushx',
            'sort',
            'sadd',
            'sdiffstore',
            'sinterstore',
            'smove',
            'spop',
            'srem',
            'sunionstore',
            'zadd',
            'zincrby',
            'zlexcount',
            'zrem',
            'zremrangebylex',
            'zremrangebyrank',
            'zremrangebyscore',
            'zunionstore',
            'pfadd',
            'pfmerge',
            'hdel',
            'hincrby',
            'hincrbyfloat',
            'hset',
            'hsetnx',
            'hmset',
            'hvals',
            'publish',
            'cluster',
            'eval',
            'evalsha',
            'script_exists',
            'script_flush',
            'script_kill',
            'script_load',
            'register_script',
            'geoadd',
        ]

    # def _get_read_operations(self):
    #     return [
    #         'bitcount',
    #         'bitpos',
    #         'dump',
    #         'exists',
    #         'get',
    #         '__getitem__',
    #         'getbit',
    #         'getrange',
    #         'keys',
    #         'mget',
    #         'pttl',
    #         'randomkey',
    #         'strlen',
    #         'substr',
    #         'linsert',
    #         'llen',
    #         'lrange',
    #         'scan',
    #         'scan_iter',
    #         'sscan',
    #         'sscan_iter',
    #         'hscan',
    #         'hscan_iter',
    #         'zscan',
    #         'zscan_iter',
    #         'scard',
    #         'sdiff',
    #         'sinter',
    #         'sismember',
    #         'smembers',
    #         'srandmember',
    #         'sunion',
    #         'zcard',
    #         'zcount',
    #         'zinterstore',
    #         'zrange',
    #         'zrangebylex',
    #         'zrevrangebylex',
    #         'zrangebyscore',
    #         'zrank',
    #         'zrevrange',
    #         'zrevrangebyscore',
    #         'zrevrank',
    #         'zscore',
    #         'pfcount',
    #         'hexists',
    #         'hget',
    #         'hgetall',
    #         'hkeys',
    #         'hlen',
    #         'hmget',
    #         'geodist',
    #         'geohash',
    #         'geopos',
    #         'georadius',
    #         'georadiusbymember',
    #     ]
