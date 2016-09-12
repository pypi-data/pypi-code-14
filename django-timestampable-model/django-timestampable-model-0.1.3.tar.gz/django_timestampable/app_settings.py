# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from django.conf import settings

TIMESTAMPABLE_MODEL_INDEX_ENABLE = getattr(settings, 'TIMESTAMPABLE_MODEL_INDEX_ENABLE', True)
