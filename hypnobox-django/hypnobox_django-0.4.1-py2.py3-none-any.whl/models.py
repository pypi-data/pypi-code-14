# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class Lead(models.Model):
    name = models.CharField(_('name'), max_length=200)
    email = models.EmailField(_('email'))
    phone_prefix = models.CharField(
        _('phone prefix'),
        max_length=3,
        validators=[RegexValidator(r'^\d{2,3}$', message=_("Only numbers."))]
    )
    phone_number = models.CharField(
        _('phone number'), max_length=10,
        validators=[RegexValidator(r'^[\d\-]+$', message=_("Only numbers."))])
    product_id = models.CharField(_('product id'), max_length=100, blank=True)
    description = models.CharField(_('description'), max_length=255, blank=True)
    media = models.CharField(_('media'), max_length=250)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('lead')
        verbose_name_plural = _('leads')

    def __unicode__(self):
        return self.name
