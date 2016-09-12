# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone


def published(queryset):
    yougner_than = timezone.now()
    queryset = queryset.filter(site__id=settings.SITE_ID)
    queryset = queryset.filter(published_on__lte=yougner_than)
    queryset = queryset.filter(is_published=True)
    return queryset


class InterviewManager(models.Manager):
    def published(self):
        return published(self.all())

    def on_site(self):
        queryset = self.filter(site__id=settings.SITE_ID)
        return queryset
