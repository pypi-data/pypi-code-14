#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2016/8/5
 """
from __future__ import unicode_literals, absolute_import
from django.utils.translation import ugettext as _


class StanderResponseError(Exception):
    """
    标准响应错误，必须包含段 status 和 msg 两个字
    data 为在发生错误的情况下需要给前端返回的数据，一般是没有的。

    0-9999 公共错误代码
    10000-19999 o2o
    20000-29999 商家版
    30000-39999 配送版
    40000-49999 供应链
    """
    def __init__(self, status, msg, data=None):
        self.status = status
        self.msg = msg
        self.data = data


class StanderCommonError(Exception):
    """
    标准响应错误，必须包含段 status 和 msg 两个字
    data 为在发生错误的情况下需要给前端返回的数据，一般是没有的。

    0-9999 公共错误代码
    10000-19999 o2o
    20000-29999 商家版
    30000-39999 配送版
    40000-49999 供应链
    """
    def __init__(self, status, msg, data=None):
        self.status = status
        self.msg = msg
        self.data = data


class StanderBackendError(Exception):
    """
    标准响应错误，必须包含段 status 和 msg 两个字
    data 为在发生错误的情况下需要给前端返回的数据，一般是没有的。

    0-9999 公共错误代码
    10000-19999 o2o
    20000-29999 商家版
    30000-39999 配送版
    40000-49999 供应链
    """
    def __init__(self, status, msg, data=None):
        self.status = status
        self.msg = msg
        self.data = data


auth_error = StanderResponseError(1, _('not authenticated'), {})


class ParameterNotExistsError(StanderResponseError):
    """
    参数不存在
    """
    def __init__(self, param):
        msg = _('Parameter {0} dose not exists.').format(param)
        super(ParameterNotExistsError, self).__init__(2, msg)
