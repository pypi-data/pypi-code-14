# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import traceback

from django.db import transaction

from .exceptions import StanderResponseError
from .Const import JavaCommonRestClient
from .models import BankVerify, VerifiedUser, BankInfo
from .serializers import BankVerifySerializers, BankInfoSerializers, VerifiedUserSerializers

logger = logging.getLogger("djdg_common_verify")

"""
Example:

    # 用户获取银行卡绑定信息
    Auther = BankCardUserAuther(user_id=1)
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    # {"statusCode": 5000, "msg": "银行卡暂未通过认证", "data": {}} 未通过认证
    # {"statusCode": 0, "msg": "成功",
        "data": {
        "bankcard": "", "bank_branch_name": "", "type": "", "province": "", "city": "",
        "tel": "", "bank_name": "", "bank_logo": "", "color": "", "name": "", "identity": ""
     }
    } 通过认证

    # 传参进行认证
    Auther = BankCardUserAuther(user_id=1, auth_data={
        "bankcard": "", "bank_branch_name": "", "type": "", "province": "", "city": "",
        "tel": "", "bank_name": "", "bank_logo": "", "color": "", "name": "", "identity": ""
     }
    # 调用认证方法
    Auther.auth()
    # 获取序列化之后的信息
    Auther.serializer()
    # 返回信息为dict
    # {"statusCode": 5000, "msg": "用户暂未通过认证", "data":{}} 未通过认证
    # {"statusCode": 0, "msg": "成功",
        "data": {
        "bankcard": "", "bank_branch_name": "", "type": "", "province": "", "city": "",
        "tel": "", "bank_name": "", "bank_logo": "", "color": "", "name": "", "identity": ""
     }
    } 通过认证
"""


class BankCardUserAuther(object):
    _validate = False
    _validate_data = {}
    UNVALIDATE = {"statusCode": 5000, "msg": "银行卡暂未通过认证", "data": {}}
    CANNOTVALIDATE = {"statusCode": 5001, "msg": "提交银行卡相关信息未通过认证", "data": {}}
    UNAUTHIDCARD = {"statusCode": 5002, "msg": "未通过实名认证", "data": {}}
    UNSUPPORTBANKTYPE = {"statusCode": 5003, "msg": "暂不支持此银行卡绑定", "data": {}}
    DATAMISSING = {"statusCode": 5004, "msg": "数据不全", "data": {}}
    COMMUNITYERROR = {"statusCode": 5005, "msg": "系统间通讯出现问题", "data": {}}
    ERROR_MSG = {}

    def __init__(self, user_id, auth_data={}):
        self.user_id = user_id
        self.auth_data = auth_data

    def __set_validate_status(self, bool_value, msg):
        self._validate = bool_value
        self.ERROR_MSG = msg

    def _checker(self):
        """
        name
        identity
        bankcard
        tel
        """
        if not self._checkidcardauth:
            return
        if not self._checkbankcardauth:
            return
        self.__set_validate_status(True, {})
        self._validate_data = {"statusCode": 0,
                               "msg": "成功",
                               "data": self._get_bankcard()
                               }

    @property
    def _checkidcardauth(self):
        from .idcard_auth import IdCardUserAuther
        id_auther = IdCardUserAuther(user_id=self.user_id).serializer()
        if id_auther["statusCode"] != 0:
            self.__set_validate_status(False, self.UNAUTHIDCARD)
            return False
        else:
            self.auth_data.update(dict(identity=id_auther["data"]["identity"]))
            return True

    @property
    def _checkbankcardauth(self):
        if not BankVerify.objects.filter(user_id=self.user_id,
                                         status=BankVerify.STATUS_AUDIT_PASS).exists():
            self.__set_validate_status(False, self.UNVALIDATE)
            return False
        else:
            return True

    def serializer(self):
        if self.ERROR_MSG:
            return self.ERROR_MSG
        self._checker()
        if self._validate:
            return self._validate_data
        else:
            return self.ERROR_MSG if self.ERROR_MSG else self.UNVALIDATE

    @property
    def _first_bindcheck(self):
        # 第一步
        if all([self.auth_data[i] for i in ["name", "bankcard", "tel"]]):
            return True
        return False

    @property
    def _second_bindcheck(self):
        # 第二步 更改银行卡支行信息
        if all([self.auth_data[i] for i in ["province", "city", "bank_branch_name"]]):
            return True
        return False

    def get_bankinfo(self):
        rest_client_resource = JavaCommonRestClient.get_resource(
            'bankcard/query/{bankcardno}'.format(bankcardno=self.auth_data["bankcard"]),
            app='certification')
        rest_client_method = rest_client_resource.get

        try:
            result = rest_client_method()
            # 获取银行卡类型
            bank_type_dict = \
                {
                    "存折": 0,
                    "借记卡": 1,
                    "信用卡": 2,
                }
            bank_type = bank_type_dict.get(result.data["cardtype"], None)
            data = result.data
            data.update(dict(bank_type=bank_type))
            return data
        except StanderResponseError:
            logger.error("请求java common api出现问题")
            return {}
        except Exception as e:
            logger.error(traceback.print_exc())
            return {}

    def auth(self):
        if not self._checkidcardauth:
            return False
        if self._first_bindcheck:
            rest_client_resource = JavaCommonRestClient.get_resource('bankcard', app='certification')
            rest_client_method = rest_client_resource.post
            try:
                result = rest_client_method(data=self.auth_data)
            except StanderResponseError:
                logger.error("请求java common api出现问题")
                self.__set_validate_status(False, self.COMMUNITYERROR)
                return False
            data = result.data
            if result.status == 0:
                # 可重新绑定银行卡
                try:
                    with transaction.atomic():
                        bank_info_data = self.get_bankinfo()
                        if not bank_info_data:
                            return False
                        if not BankInfo.objects.filter(name=data['bankname']).exists():
                            self.__set_validate_status(False, self.UNSUPPORTBANKTYPE)
                            return False
                        bank_info_obj = BankInfo.objects.filter(name=data['bankname']).first()
                        BankVerify.objects.filter(user_id=self.user_id,
                                                  status=BankVerify.STATUS_AUDIT_PASS).update(
                            status=BankVerify.STATUS_NOT_USE)
                        BankVerify.objects.create(user_id=self.user_id,
                                                  bank_info=bank_info_obj,
                                                  card_no=self.auth_data["bankcard"],
                                                  card_tel=self.auth_data["tel"],
                                                  type=bank_info_data["bank_type"] \
                                                      if bank_info_data["bank_type"] is not None else 1,
                                                  status=BankVerify.STATUS_AUDIT_PASS)
                        self._checker()
                        return True
                except Exception:
                    logger.error("请求java common api出现问题")
                    logger.error(traceback.print_exc())
                    self.__set_validate_status(False, self.COMMUNITYERROR)
                    return False
            else:
                self.__set_validate_status(False, self.COMMUNITYERROR)
                return False
        elif self._second_bindcheck:
            if not self._checkbankcardauth:
                return False
            BankVerify.objects.filter(user_id=self.user_id,
                                      status=BankVerify.STATUS_AUDIT_PASS).update(
                card_branch=self.auth_data['bank_branch_name'],
                province=self.auth_data['province'],
                city=self.auth_data['city'])
            return True
        else:
            self.__set_validate_status(False, self.DATAMISSING)
            return False

    def _get_bankcard(self):
        # bankverify_dict = {"bankcard": "",
        #                    "bank_branch_name": "",
        #                    "type": "",
        #                    "province": "",
        #                    "city": "",
        #                    "tel": ""}
        # bankinfo_dict = {
        #     "bank_name": "",
        #     "bank_logo": "",
        #     "color": ""
        # }
        # verifieduser_dict = {
        #     "name": "",
        #     "identity": ""
        # }
        userpayinfo_dict = {
            "transaction_pwd_status": 0
        }
        bankverify_obj = BankVerify.objects.get(user_id=self.user_id, status=0)
        verifieduser_obj = VerifiedUser.objects.get(user_id=self.user_id, status=0)
        if verifieduser_obj.pay_password:
            userpayinfo_dict.update({"transaction_pwd_status": 1})
        else:
            userpayinfo_dict.update({"transaction_pwd_status": 0})
        bank_obj = {}
        bank_obj.update(dict(BankVerifySerializers(bankverify_obj).data))
        bank_obj.update(dict(BankInfoSerializers(bankverify_obj.bank_info).data))
        bank_obj.update(userpayinfo_dict)
        bank_obj.update(dict(VerifiedUserSerializers(verifieduser_obj).data))
        return bank_obj
