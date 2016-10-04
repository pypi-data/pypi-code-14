# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from publishing.mixins import PublishingModelMixin


class Category(models.Model):
    title = models.CharField("Title", max_length=255, )

    def __str__(self):
        return u"CATEGORY: %s" % self.title


class Topic(models.Model):
    title = models.CharField("Title", max_length=255, )

    def __str__(self):
        return u"TOPIC: %s" % self.title


class Tag(PublishingModelMixin,
          models.Model):
    title = models.CharField("Title", max_length=255, )
    blog = models.ForeignKey("Blog", related_name='blog_tags', null=True, blank=True, )

    def __str__(self):
        return u"TAG: %s" % self.title


class Blog(PublishingModelMixin,
           models.Model):

    title = models.CharField("Title", max_length=255, )
    category = models.ForeignKey("Category", null=True, blank=True, )
    topics = models.ManyToManyField("Topic", null=True, blank=True, )

    def __str__(self):
        return u"BLOG: %s" % self.title


