# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction

from .exceptions import StanderResponseError
from .Const import JavaCommonRestClient
from .models import VerifiedUser
from .utils.cache import ActionKeyOperation
import logging

logger = logging.getLogger("djdg_common_verify")


"""
Example:

    # 用户获取银行卡绑定信息
    Auther = UserPasswordAuther(user_id=1)
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    # {"statusCode": 0, "msg": "成功", "data": {"password": "设置的密码"}} 已经设置密码
    # {"statusCode": 5000, "msg": "用户暂未设置交易密码", "data": {}} 未设置密码

    # 传参进行认证
    # 设置交易密码 (之前尚未设置交易密码)
    Auther = UserPasswordAuther(user_id=1, auth_data={"password":"设置的交易密码"})
    # 调用认证方法
    Auther.auth()
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    # {"statusCode": 5006, "msg": "密码无效或者为空", "data": {}} 未通过认证
    # {"statusCode": 0, "msg": "成功", "data": {"password": "设置的密码"}} 通过认证

    # 修改交易密码 (之前已经设置交易密码)
    # 第一步获取settingtoken
    Auther = UserPasswordAuther(user_id=1, auth_data={"identity":"身份证号码"})
    # 调用获取settingtoken方法
    Auther.get_settingtoken
    # 返回信息为dict
    {"statusCode": 5003, "msg": "用户身份证信息未通过校验", "data": {}}
    {"statusCode": 5000, "msg": "用户暂未设置交易密码", "data": {}}
    {"statusCode": 0,
                "msg": "验证身份信息成功",
                "data": {
                    "settingToken": settingtoken.token
                }}  # 获取成功返回信息
    # 第一步获取settingtoken
    Auther = UserPasswordAuther(user_id=1, auth_data={"password":"设置的交易密码", "setttingtoken":"通过第一步获取的settingtoken"})
    # 调用认证方法
    Auther.auth()
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    # {"statusCode": 5001, "msg": "setting token未通过校验", "data": {}} 未通过认证
    # {"statusCode": 5005, "msg": "settingtoken失效", "data": {}} 未通过认证
    # {"statusCode": 0, "msg": "成功", "data": {"password": "设置的密码"}} 通过认证

"""


class UserPasswordAuther(object):
    _validate = False
    _validate_data = {}
    UNVALIDATE = {"statusCode": 5000, "msg": "用户暂未设置交易密码", "data": {}}
    CANNOTVALIDATE = {"statusCode": 5001, "msg": "setting token未通过校验", "data": {}}
    COMMUNITYERROR = {"statusCode": 5002, "msg": "系统间通讯出现问题", "data": {}}
    UNAUTHIDINFO = {"statusCode": 5003, "msg": "用户身份证信息未通过校验", "data": {}}
    IDNOMISSING = {"statusCode": 5004, "msg": "身份信息未传入", "data": {}}
    TOKENMISSING = {"statusCode": 5005, "msg": "settingtoken未传入", "data": {}}
    TOKENFAIL = {"statusCode": 5006, "msg": "settingtoken失效", "data": {}}
    PASSWORDVALID = {"statusCode": 5007, "msg": "密码无效或者为空", "data": {}}
    ERROR_MSG = {}

    def __init__(self, user_id, auth_data=None):
        self.user_id = user_id
        self.auth_data = auth_data

    def __set_validate_status(self, bool_value, msg):
        self._validate = bool_value
        self.ERROR_MSG = msg

    def _check_verify(self):
        try:
            id_card_no = self.auth_data["identity"]
        except KeyError:
            self.__set_validate_status(False, self.IDNOMISSING)
            return False
        if not VerifiedUser.objects.filter(user_id=self.user_id, id_card_no=id_card_no).exists():
            self.__set_validate_status(False, self.UNAUTHIDINFO)
            return False
        return True

    def get_settingtoken(self):
        if not self._check_verify():
            return self.serializer()
        settingtoken = ActionKeyOperation(key_type="settingpassword", app_type="modifypassword",
                                          action_type="settingtoken", expire=60 * 10, user_id=self.user_id)
        settingtoken.settoken()
        return {"statusCode": 0,
                "msg": "验证身份信息成功",
                "data": {
                    "settingToken": settingtoken.token
                }}

    def _checker(self):
        if VerifiedUser.objects.filter(user_id=self.user_id,
                                       status=VerifiedUser.STATUS_AUDIT_PASS).exists():
            v_obj = VerifiedUser.objects.filter(user_id=self.user_id,
                                                status=VerifiedUser.STATUS_AUDIT_PASS).first()
            if v_obj.pay_password:
                self.__set_validate_status(True, {"statusCode": 0,
                                                  "msg": "成功",
                                                  "data": {"password": v_obj.pay_password}})
                self._validate_data = {"statusCode": 0,
                                       "msg": "成功",
                                       "data": {"password": v_obj.pay_password}}
            else:
                self.__set_validate_status(False, self.UNVALIDATE)

    def serializer(self):
        if self.ERROR_MSG:
            return self.ERROR_MSG
        self._checker()
        if self._validate:
            return self._validate_data
        else:
            return self.ERROR_MSG if self.ERROR_MSG else self.UNVALIDATE

    @property
    def _hassettingtoken(self):
        if "settingToken" in self.auth_data:
            return True
        else:
            return False

    @property
    def _modifypassword(self):
        if VerifiedUser.objects.filter(user_id=self.user_id,
                                       status=VerifiedUser.STATUS_AUDIT_PASS).exclude(pay_password=None).exists():
            return True
        return False

    @property
    def _setpassword(self):
        if VerifiedUser.objects.filter(user_id=self.user_id,
                                       status=VerifiedUser.STATUS_AUDIT_PASS, pay_password=None).exists():
            return True
        return False

    def __setmodel_password(self):
        # 直接使用前端传入的密码进行保存
        v = VerifiedUser.objects.filter(user_id=self.user_id,
                                        status=VerifiedUser.STATUS_AUDIT_PASS)[0]
        if not isinstance(self.auth_data["password"], str):
            self.__set_validate_status(False, self.PASSWORDVALID)
            return False
        if not self.auth_data["password"]:
            self.__set_validate_status(False, self.PASSWORDVALID)
            return False
        v.pay_password = self.auth_data["password"]
        v.save()
        return True

    def auth(self):
        if self._modifypassword:
            if self._hassettingtoken:
                settingtoken = ActionKeyOperation(key_type="settingpassword", app_type="modifypassword",
                                                  action_type="settingtoken", expire=60 * 10, user_id=self.user_id)
                if not settingtoken.token:
                    self.__set_validate_status(False, self.TOKENFAIL)
                    return False
                if settingtoken.token != self.auth_data["settingtoken"]:
                    self.__set_validate_status(False, self.CANNOTVALIDATE)
                    return False
                return self.__setmodel_password()

            else:
                self.__set_validate_status(False, self.TOKENMISSING)
                return False
        if self._setpassword:
            return self.__setmodel_password()
