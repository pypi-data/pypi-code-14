# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy as Flask_SQLAlchemy
from .globals import *
from flask import request
from sqlalchemy import event
from sqlalchemy.orm import mapper
from sqlalchemy.inspection import inspect
from diandao import isint_or


class SQLAlchemy(Flask_SQLAlchemy):
    def __init__(self, app=None, use_native_unicode=True, session_options=None, metadata=None):
        """重构父级初始化方法,缓存app对象"""
        super(self.__class__, self).__init__(app, use_native_unicode, session_options, metadata)
        if app is not None:
            apply_app(app)
        pass

    def init_app(self, app):
        """重构父级初始化方法,缓存app对象"""
        super(self.__class__, self).init_app(app)
        if app is not None:
            apply_app(app)
        pass


def apply_app(app):
    stacker["app"] = app
    app.config.setdefault("CACHE_LIFE_TIME", 600)


class BaseInterface(object):
    """基础接口类"""
    # 绑定指定模型类, 可继承模型的类方法(@classmethod)
    __bindmodel__ = None

    def __getattr__(self, name):
        if self.__bindmodel__ is not None:
            return getattr(self.__bindmodel__, name, None)
        return None


class version_control:
    def __getattribute__(self, name):  # real signature unknown; restored from __doc__
        """ x.__getattribute__('name') <==> x.name """
        pass

    def __get__(self, obj, type=None):  # real signature unknown; restored from __doc__
        """ descr.__get__(obj[, type]) -> value """
        pass

    def __set__(self, obj, type=None):  # real signature unknown; restored from __doc__
        """ descr.__get__(obj[, type]) -> value """
        pass

    def __del__(self, obj, type=None):  # real signature unknown; restored from __doc__
        """ descr.__get__(obj[, type]) -> value """
        pass

    def __init__(self, function):  # real signature unknown; restored from __doc__
        pass

    __func__ = property(__get__, __set__, __del__)  # default


def version(ver):
    """版本号修饰"""
    return version_control

def operator_role():
    """请求头消息中获取操作者数据"""
    return  request.headers.get("Operator-Role", "")

def operator_id():
    """请求头消息中获取操作者数据"""
    return  request.headers.get("Operator-Id", 0)

def instant_defaults_listener(target, args, kwargs):
    """
    模型初始化时, 字段使用默认值
    """
    for key, column in inspect(target.__class__).columns.items():
        # if key in ["creatorid", "operatorid"]:
        #     # 请求头消息中获取操作者数据, 自动填入creatorid, operatorid字段
        #     operatorid = operator_id()
        #     if operatorid is not None:
        #         setattr(target, key, operatorid)
        #         continue
        # # operator role
        # if key in ["creator_role", "operator_role"]:
        #     # 请求头消息中获取操作者数据, 自动填入creatorid, operatorid字段
        #     role = operator_role()
        #     if operatorrole is not None:
        #         setattr(target, key, role)
        #         continue

        if column.default is not None:
            if callable(column.default.arg):
                setattr(target, key, column.default.arg(target))
            else:
                setattr(target, key, column.default.arg)

# 默认值初始化
event.listen(mapper, 'init', instant_defaults_listener)