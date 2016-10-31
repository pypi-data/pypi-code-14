# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth.models import User
from .bankcard_auth import BankCardUserAuther
from .idcard_auth import IdCardUserAuther
from .paypassword_auth import UserPasswordAuther


class IdCardUserAutherTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="fredzhang", password="123456")

    def test_not_auth_serialier(self):
        Auther = IdCardUserAuther(user_id=self.user.id)
        self.assertEqual({"statusCode": 5000, "msg": "用户暂未通过认证", "data": {}}, Auther.serializer())

    def test_success_auth(self):
        Auther = IdCardUserAuther(user_id=self.user.id, auth_data={"name": "熊小燕", "identity": "362203197704084720"})
        self.assertEqual(True, Auther.auth())

    def test_success_auth_serializer(self):
        Auther = IdCardUserAuther(user_id=self.user.id, auth_data={"name": "熊小燕", "identity": "362203197704084720"})
        Auther.auth()
        self.assertEqual({'data': {'identity': '362203197704084720', 'name': "熊小燕"},
                          "msg": "成功",
                          'statusCode': 0},
                         Auther.serializer())

    def test_auth_fail(self):
        Auther = IdCardUserAuther(user_id=self.user.id, auth_data={"name": "熊小燕", "identity": "3622031977040847201"})
        self.assertEqual(False, Auther.auth())

    def test_auth_fail_serializer(self):
        Auther = IdCardUserAuther(user_id=self.user.id, auth_data={"name": "熊小燕", "identity": "3622031977040847201"})
        Auther.auth()
        self.assertEqual({'data': {},
                          "msg": "提交信息未通过认证",
                          'statusCode': 5001}, Auther.serializer())

    def tearDown(self):
        self.user.delete()


class BankCardUserAutherTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        # 创建新用户
        self.user = User.objects.create(username="fredzhang", password="123456")
        # 实名认证
        Auther = IdCardUserAuther(user_id=self.user.id, auth_data={"name": "熊小燕", "identity": "362203197704084720"})
        Auther.auth()

    def test_no_auth(self):
        Auther = BankCardUserAuther(user_id=self.user.id)
        self.assertEqual({"statusCode": 5000, "msg": "银行卡暂未通过认证", "data": {}}, Auther.serializer())

    def test_first_auth_success(self):
        Auther = BankCardUserAuther(user_id=self.user.id, auth_data={"bankcard": "9558804000161101544",
                                                                     "bank_branch_name": "", "type ": "",
                                                                     "province": "", "city": "",
                                                                     "tel": "13418951220", "bank_name": "",
                                                                     "bank_logo": "", "color": "", "name": "熊小燕",
                                                                     "identity": ""})

        self.assertEqual(True, Auther.auth())
        data = {u'data': {u'bank_branch_name': None,
                          u'bank_logo': u'http://image.thy360.com/images/bank/logo/gong_shang3.png',
                          u'bank_name': u'\u5de5\u5546\u94f6\u884c',
                          u'bankcard': u'9558804000161101544',
                          u'city': u'',
                          u'color': u'E45260',
                          u'identity': u'362203197704084720',
                          u'name': u'\u718a\u5c0f\u71d5',
                          u'province': u'',
                          u'tel': u'13418951220',
                          u'transaction_pwd_status': 0,
                          u'type': u'\u501f\u8bb0\u5361'},
                u'msg': u'\u6210\u529f',
                u'statusCode': 0}
        self.assertEqual(data, Auther.serializer())

    def test_first_auth_fail(self):
        Auther = BankCardUserAuther(user_id=self.user.id, auth_data={"bankcard": "95588040001611015440",
                                                                     "bank_branch_name": "", "type ": "",
                                                                     "province": "", "city": "",
                                                                     "tel": "13418951220", "bank_name": "",
                                                                     "bank_logo": "", "color": "", "name": "熊小燕",
                                                                     "identity": ""})
        self.assertEqual(False, Auther.auth())
        self.assertEqual({"statusCode": 5005, "msg": "系统间通讯出现问题", "data": {}}, Auther.serializer())

    def test_second_auth_success(self):
        Auther = BankCardUserAuther(user_id=self.user.id, auth_data={"bankcard": "9558804000161101544",
                                                                     "bank_branch_name": "", "type ": "",
                                                                     "province": "", "city": "",
                                                                     "tel": "13418951220", "bank_name": "",
                                                                     "bank_logo": "", "color": "", "name": "熊小燕",
                                                                     "identity": ""})

        Auther.auth()
        Auther = BankCardUserAuther(user_id=self.user.id, auth_data={"bankcard": "",
                                                                     "bank_branch_name": "test", "type ": "",
                                                                     "province": "test", "city": "test",
                                                                     "tel": "", "bank_name": "",
                                                                     "bank_logo": "", "color": "", "name": "",
                                                                     "identity": ""})
        self.assertEqual(True, Auther.auth())
        self.assertEqual({u'msg': u'\u6210\u529f',
                          u'data': {u'province': u'test', u'city': u'test', u'tel': u'13418951220',
                                    u'name': u'\u718a\u5c0f\u71d5', u'bank_name': u'\u5de5\u5546\u94f6\u884c',
                                    u'color': u'E45260', u'bankcard': u'9558804000161101544',
                                    u'bank_branch_name': u'test',
                                    u'bank_logo': u'http://image.thy360.com/images/bank/logo/gong_shang3.png',
                                    u'transaction_pwd_status': 0, u'type': u'\u501f\u8bb0\u5361',
                                    u'identity': u'362203197704084720'}, u'statusCode': 0}, Auther.serializer())

    def test_second_auth_fail(self):
        Auther = BankCardUserAuther(user_id=self.user.id, auth_data={"bankcard": "9558804000161101544",
                                                                     "bank_branch_name": "", "type ": "",
                                                                     "province": "", "city": "",
                                                                     "tel": "13418951220", "bank_name": "",
                                                                     "bank_logo": "", "color": "", "name": "熊小燕",
                                                                     "identity": ""})

        Auther.auth()
        Auther = BankCardUserAuther(user_id=self.user.id, auth_data={"bankcard": "",
                                                                     "bank_branch_name": "", "type ": "",
                                                                     "province": "test", "city": "test",
                                                                     "tel": "", "bank_name": "",
                                                                     "bank_logo": "", "color": "", "name": "",
                                                                     "identity": ""})
        self.assertEqual(False, Auther.auth())
        self.assertEqual({u'data': {}, u'msg': u'\u6570\u636e\u4e0d\u5168', u'statusCode': 5004}, Auther.serializer())

    def tearDown(self):
        self.user.delete()


class PayPasswordAutherTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None
        # 创建新用户
        self.user = User.objects.create(username="fredzhang", password="123456")
        # 实名认证
        Auther = IdCardUserAuther(user_id=self.user.id, auth_data={"name": "熊小燕", "identity": "362203197704084720"})
        Auther.auth()

    def test_not_set_password(self):
        Auther = UserPasswordAuther(user_id=self.user.id)
        self.assertEqual({"statusCode": 5000, "msg": "用户暂未设置交易密码", "data": {}}, Auther.serializer())

    def test_set_password(self):
        Auther = UserPasswordAuther(user_id=self.user.id, auth_data={"password": "321654"})
        Auther.auth()
        self.assertEqual({"statusCode": 0, "msg": "成功", "data": {"password": "321654"}}, Auther.serializer())

    def test_modify_password(self):
        Auther = UserPasswordAuther(user_id=self.user.id, auth_data={"password": "654321"})
        Auther.auth()
        print(Auther.serializer())
        Auther = UserPasswordAuther(user_id=self.user.id, auth_data={"identity": "362203197704084720"})
        settingtoken = Auther.get_settingtoken()["data"]["settingToken"]
        Auther = UserPasswordAuther(user_id=1,
                                    auth_data={"password": "987654", "settingToken": settingtoken})
        # 调用认证方法
        Auther.auth()
        # 获取序列化之后的信息
        Auther.serializer()
        self.assertEqual({"statusCode": 0, "msg": "成功", "data": {"password": "987654"}}, Auther.serializer())

    def tearDown(self):
        self.user.delete()
