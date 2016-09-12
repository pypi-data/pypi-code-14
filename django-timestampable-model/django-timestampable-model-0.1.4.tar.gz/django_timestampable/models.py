# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import django
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy
if django.VERSION >= (1, 9, 0):
    from django.db.models.functions import Now
    now = Now
else:
    from django.utils.timezone import now

from .app_settings import *


class TimestampableModel(models.Model):
    created_at = models.DateTimeField(ugettext_lazy('created at'),
                                      editable=False,
                                      db_index=TIMESTAMPABLE_MODEL_INDEX_ENABLE)
    updated_at = models.DateTimeField(ugettext_lazy('last updated at'),
                                      editable=False,
                                      db_index=TIMESTAMPABLE_MODEL_INDEX_ENABLE)

    class Meta:
        abstract = True


@receiver(pre_save)
def update_timestampable_model(sender, instance, *args, **kwargs):
    '''
    Using signals guarantees that timestamps are set no matter what:
    loading fixtures, bulk inserts, bulk updates, etc.
    Indeed, the `save()` method is *not* called when using fixtures.
    '''
    if not isinstance(instance, TimestampableModel):
        return
    if not instance.pk:
        instance.created_at = now()
    instance.updated_at = now()
