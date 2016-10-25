# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .api_info import ApiInfo


class UserBehavior(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    api_info = models.ForeignKey(
        ApiInfo, related_name='user_behaviors', db_constraint=False, null=True)

    class Meta:
        db_table = 'user_behavior'
