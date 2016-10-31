# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import traceback
from django.db import transaction

from .exceptions import StanderResponseError
from .Const import JavaCommonRestClient
from .models import VerifiedUser
from .serializers import VerifiedUserSerializers


logger = logging.getLogger("djdg_common_verify")

"""
# 如果将返回的数据直接作为Response进行返回的时候，使用rest-frameword的Response方法进行返回

Example:

    # 用户获取实名认证信息
    Auther = IdCardUserAuther(user_id=1)
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    # {"statusCode": 5000, "msg": "用户暂未通过认证", "data":{}} 未通过认证
    # {"statusCode": 0, "msg": "成功", "data":{"name":"张三", "identity":1234}} 通过认证

    # 传参进行认证
    Auther = IdCardUserAuther(user_id=1, auth_data={"name":"张三", "identity":"123456789"})
    # 调用认证方法
    Auther.auth()
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    # {"statusCode": 5000, "msg": "用户暂未通过认证", "data":{}} 未通过认证
    # {"statusCode": 0, "msg": "成功", "data":{"name":"张三", "identity":1234}} 通过认证

"""


class IdCardUserAuther(object):
    _validate = False
    _validate_data = {}
    UNVALIDATE = {"statusCode": 5000, "msg": "用户暂未通过认证", "data":{}}
    CANNOTVALIDATE = {"statusCode": 5001, "msg": "提交信息未通过认证", "data": {}}
    COMMUNITYERROR = {"statusCode": 5002, "msg": "系统间通讯出现问题", "data": {}}
    ERROR_MSG = {}

    def __init__(self, user_id, auth_data=None):
        self.user_id = user_id
        self.auth_data = auth_data

    def __set_validate_status(self, bool_value, msg):
        self._validate = bool_value
        self.ERROR_MSG = msg

    def _checker(self):
        if VerifiedUser.objects.filter(user_id=self.user_id,
                                       status=VerifiedUser.STATUS_AUDIT_PASS).exists():
            self.__set_validate_status(True, {})
            data = VerifiedUserSerializers(
                                       VerifiedUser.objects.filter(user_id=self.user_id,
                                                                   status=0)[0]).data
            data = dict(data)
            self._validate_data = {"statusCode": 0,
                                   "msg": "成功",
                                   "data": data
                                   }

    def serializer(self):
        if self.ERROR_MSG:
            return self.ERROR_MSG
        self._checker()
        if self._validate:
            return self._validate_data
        else:
            return self.ERROR_MSG if self.ERROR_MSG else self.UNVALIDATE

    def auth(self):
        rest_client_resource = JavaCommonRestClient.get_resource('idcard', app='certification')
        rest_client_method = rest_client_resource.post
        try:
            result = rest_client_method(data=self.auth_data)
        except StanderResponseError:
            logger.error("请求java common api出现问题")
            self.__set_validate_status(False, self.CANNOTVALIDATE)
            return False
        if result.status == 0:
            # 可重新实名认证
            try:
                with transaction.atomic():
                    VerifiedUser.objects.filter(user_id=self.user_id,
                                                status=VerifiedUser.STATUS_AUDIT_PASS).\
                        delete()
                    VerifiedUser.objects.create(
                        user_id=self.user_id,
                        id_name=self.auth_data['name'],
                        id_card_no=self.auth_data['identity'],
                        type=VerifiedUser.TYPE_REAL_NAME_VALIDATE,
                        status=VerifiedUser.STATUS_AUDIT_PASS,
                    )
                    self._checker()
                    return True
            except Exception as e:
                logger.error("error:{msg}".format(msg=traceback.print_exc()))
                logger.error("操作数据库出现问题")
                self.__set_validate_status(False, self.COMMUNITYERROR)
                return False

        else:
            return False



