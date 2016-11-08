# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from .models import BankInfo, BankVerify, VerifiedUser


class BankInfoSerializers(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='name', read_only=True)
    bank_logo = serializers.CharField(source='logo', read_only=True)

    class Meta:
        model = BankInfo
        fields = ("bank_name", "bank_logo", "color")


class BankVerifySerializers(serializers.ModelSerializer):
    bankcard = serializers.CharField(source='card_no')
    bank_branch_name = serializers.CharField(source='card_branch')
    type = serializers.SerializerMethodField()
    tel = serializers.CharField(source="card_tel")

    class Meta:
        model = BankVerify
        fields = ("bankcard", "bank_branch_name", "type", "province",
                  "city", "tel")

    def get_type(self, obj):
        return obj.get_type_display()


class VerifiedUserSerializers(serializers.ModelSerializer):
    name = serializers.CharField(source='id_name')
    identity = serializers.CharField(source='id_card_no')

    class Meta:
        model = VerifiedUser
        fields = ("name", "identity")
