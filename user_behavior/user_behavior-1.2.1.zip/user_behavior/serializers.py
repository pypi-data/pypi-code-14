# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import serializers

from .base import DynamicFieldsModelSerializer, UserField

from .models.api_info import ApiInfo
from .models.user_behavior import UserBehavior


class ApiInfoSerializer(DynamicFieldsModelSerializer):
    user = UserField()
    user_behaviors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ApiInfo
        read_only_fields = ('response',)


class UserBehaviorSerializer(DynamicFieldsModelSerializer):
    action = serializers.SerializerMethodField()

    class Meta:
        model = UserBehavior
        fields = ('id', 'created_at', 'updated_at', 'action', 'api_info')
        depth = 1

    def get_action(self, obj):
        return {
            'app_label': obj.content_type.app_label,
            'model': obj.content_type.model,
            'object_id': obj.object_id,
            'object_detail': self.get_object_detail(obj),
        }

    def get_object_detail(self, obj):
        try:
            record = obj.content_type.get_object_for_this_type(id=obj.object_id)
        except:
            return {}

        from django.forms import model_to_dict
        records = model_to_dict(record)

        return records
