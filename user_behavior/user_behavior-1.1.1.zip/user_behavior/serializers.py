# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import serializers

from .models.api_info import ApiInfo
from .models.user_behavior import UserBehavior


class ApiInfoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='last_name')

    class Meta:
        model = ApiInfo


class UserBehaviorSerialier(serializers.ModelSerializer):

    class Meta:
        model = UserBehavior
