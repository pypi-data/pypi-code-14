# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rest_framework import serializers

from django.utils import timezone

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class DateTimeFormatField(serializers.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs['format'] = DATE_FORMAT
        return super(DateTimeFormatField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFormatField, self).to_representation(value)


class UserField(serializers.Field):

    def to_representation(self, obj):
        return {
            'username': obj.username,
            'first_name': obj.first_name,
            'last_name': obj.last_name,
            'email': obj.email,
            'is_superuser': obj.is_superuser,
        }
