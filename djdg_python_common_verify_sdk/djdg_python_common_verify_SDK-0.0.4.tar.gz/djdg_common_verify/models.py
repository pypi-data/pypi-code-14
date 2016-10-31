# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class VerifiedUser(models.Model):
    """
    身份认证信息
    """
    TYPE_REAL_NAME_VALIDATE = 0
    TYPE_UPLOAD_VALIDATE = 1
    CHOICE_TYPE = (
        (TYPE_REAL_NAME_VALIDATE, '实名认证'),
        (TYPE_UPLOAD_VALIDATE, '上传认证')
    )
    STATUS_AUDIT_PASS = 0
    STATUS_AUDIT = 1
    STATUS_NOT_USE = 2
    STATUS_RE_AUDIT = 4
    CHOICE_STATUS = (
        (STATUS_AUDIT_PASS, '认证成功'),
        (STATUS_AUDIT, '待审核'),
        (STATUS_NOT_USE, '未使用'),
        (STATUS_RE_AUDIT, '认证失败')
    )
    user = models.OneToOneField(User, related_name="common_verified_user")
    id_name = models.CharField(u"身份证姓名", max_length=64, null=True)
    id_card_no = models.CharField(u"身份证号码", max_length=32, null=True)
    type = models.SmallIntegerField(u"认证类型", default=0, choices=CHOICE_TYPE)
    id_card_img1 = models.CharField(u"身份证正面", max_length=128, null=True)
    id_card_img2 = models.CharField(u"身份证反而", max_length=128, null=True)
    status = models.SmallIntegerField(u"认证状态", default=0, choices=CHOICE_STATUS)
    stime = models.DateTimeField(u"状态时间", auto_now=True)
    ctime = models.DateTimeField(u"创建时间", auto_now_add=True)
    pay_password = models.CharField(u"支付密码", max_length=128, null=True, blank=True)

    @classmethod
    def has_verified(cls, user):
        return cls.objects.filter(user=user, status=0).exists()


class BankInfo(models.Model):
    """
    银行信息
    """
    name = models.CharField(u"银行名称", max_length=32)
    logo = models.CharField(u"银行LOGO URL", max_length=255)
    color = models.CharField(u"银行卡底色", max_length=8, default='FFFFFF')


class BankVerify(models.Model):
    TYPE_BANK_BOOK = 0
    TYPE_DEBIT_CARD = 1
    TYPE_CREDIT_CARD = 2
    CHOICE_TYPE = (
        (TYPE_BANK_BOOK, '存折'),
        (TYPE_DEBIT_CARD, '借记卡'),
        (TYPE_CREDIT_CARD, '信用卡')
    )
    STATUS_AUDIT_PASS = 0
    STATUS_AUDIT = 1
    STATUS_NOT_USE = 2
    STATUS_RE_AUDIT = 4
    CHOICE_STATUS = (
        (STATUS_AUDIT_PASS, '绑定成功'),
        (STATUS_AUDIT, '绑定中'),
        (STATUS_NOT_USE, "未使用"),
        (STATUS_RE_AUDIT, '绑定失败')
    )
    user = models.ForeignKey(User)
    bank_info = models.ForeignKey(BankInfo, related_name="dealer_bank_card", null=True, default=None,
                                  on_delete=models.SET_NULL)
    card_branch = models.TextField("开户支行", max_length=64, null=True)
    province = models.CharField("省份", max_length=32, default='')
    city = models.CharField("城市", max_length=16, default='')
    card_no = models.CharField("卡号", max_length=64)
    card_tel = models.CharField("预留手机", max_length=16)
    type = models.SmallIntegerField("卡类型", default=1, choices=CHOICE_TYPE)
    status = models.SmallIntegerField("卡状态", default=0, choices=CHOICE_STATUS)
    stime = models.DateTimeField("状态时间", auto_now=True)
    ctime = models.DateTimeField("创建时间", auto_now_add=True)

