# -*- coding: utf-8 -*-
from django.db import models
from metaset.django_field import MetaSetField


class TestModel(models.Model):
    value = MetaSetField()
