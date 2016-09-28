# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DiscountsCartConfig(AppConfig):
    name = 'discounts_cart'
    verbose_name = _('Discounts')
