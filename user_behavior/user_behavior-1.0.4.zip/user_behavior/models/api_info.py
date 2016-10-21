# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


class ApiInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    client = JSONField(default={}, null=True, blank=True)
    server = JSONField(default={}, null=True, blank=True)
    request = JSONField(default={}, null=True, blank=True)
    response = JSONField(default={}, null=True, blank=True)
    user = models.ForeignKey(
        User, related_name='user_behaviors', db_constraint=False, null=True)

    class Meta:
        db_table = 'api_info'
