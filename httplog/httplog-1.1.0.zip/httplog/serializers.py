# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import serializers

from .base import DynamicFieldsModelSerializer, UserField

from .models.httplog import HttpLog


class HttpLogSerializer(DynamicFieldsModelSerializer):
    user = UserField()

    class Meta:
        model = HttpLog
        read_only_fields = ('response',)
