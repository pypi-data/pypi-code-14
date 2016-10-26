# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import serializers

from .base import DateTimeFormatField, UserField

from .models.api_info import ApiInfo
from .models.user_behavior import UserBehavior


class ApiInfoSerializer(serializers.ModelSerializer):
    created_at = DateTimeFormatField()
    updated_at = DateTimeFormatField()
    user = UserField()

    class Meta:
        model = ApiInfo


class UserBehaviorSerializer(serializers.ModelSerializer):
    created_at = DateTimeFormatField()
    updated_at = DateTimeFormatField()
    operation = serializers.SerializerMethodField()

    class Meta:
        model = UserBehavior
        exclude = ('content_type',)

    def get_operation(self, obj):
        return {
            'app_label': obj.content_type.app_label,
            'model': obj.content_type.model,
        }
