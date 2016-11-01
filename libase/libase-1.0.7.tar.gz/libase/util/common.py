#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   common.py
Author:     Chen Yanfei
@contact:   gzchenyanfei@corp.netease.com
@version:   $Id$

Description:

Changelog:

'''

import os
import sys
import json
import signal
import socket
import time
import logging
import traceback


class Object(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class NullContext(object):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

null_context = NullContext()


def iteratable(obj):
    return bool(getattr(obj, '__iter__', None))


def list_or_tuple(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)


def ensure_string(string, encoding='utf8'):
    return string.encode(encoding) if isinstance(string, unicode) else string


def ensure_unicode(string, encoding='utf8'):
    return string if isinstance(string, unicode) else string.decode(encoding)


def filter_dict(dict_object, filter=lambda x: x):
    for key, value in dict_object.iteritems():
        dict_object[key] = filter(value)
    return dict_object


def readable_json(data):
    '''
    可读的json序列化
    1. 缩进
    2. 中文不用Unicode编码

    data - 数据，可以是任何可json序列号的Python内建数据类型
    '''
    return json.dumps(data, ensure_ascii=False, indent=4)


def wait_until_interrupt():
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return


def call_catch_exc_detail(func, limit=None, args=(), kwargs={}):
    '''
    异常详情捕获修饰器
    捕获函数执行抛出的异常并在日志输出函数名、调用参数、异常详情

    func - 被修饰函数
    '''
    try:
        return func(*args, **kwargs)
    except Exception:
        logging.error('{module}.{func}(*{args}, **{kwargs}): {tb}'.format(
            module=func.func_globals.get('__name__', ''),
            func=func.__name__,
            args=str(args)[:limit] if limit else args,
            kwargs=str(kwargs)[:limit] if limit else kwargs,
            tb=traceback.format_exc(),
            ))


def kill_self(signo=signal.SIGTERM):
    return os.kill(os.getpid(), signo)


def on_signal(signum, callback, args=None, kwargs=None):
    args = () if args is None else args
    kwargs = {} if kwargs is None else kwargs

    def sig_handler(signum, frame):
        callback(*args, **kwargs)

    signal.signal(signum, sig_handler)


def on_sigterm(callback, args=None, kwargs=None):
    on_signal(signum=signal.SIGTERM, callback=callback, args=args, kwargs=kwargs)
