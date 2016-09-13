# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 NZME
#

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConstanceCliConfig(AppConfig):
    name = 'constance_cli'
    verbose_name = _('Constance CLI')
