#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See the file COPYING for details.

import hashlib
import random

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext
from django.template.defaultfilters import slugify


def get_cache(cls, extra_args=[]):
    cache_key = u"{}-{}-{}".format(
        settings.PROJECT_SLUG, cls._meta.app_label, cls.__name__)
    for arg in extra_args:
        if not arg:
            cache_key += '-0'
        else:
            if type(arg) == dict:
                cache_key += '-' + "_".join([unicode(arg[k]) for k in arg])
            elif type(arg) in (list, tuple):
                cache_key += '-' + "_".join([unicode(v) for v in arg])
            else:
                cache_key += '-' + unicode(arg)
    cache_key = slugify(cache_key)
    if not cache_key.endswith('_current_keys') \
            and hasattr(cls, '_add_cache_key_to_refresh'):
        cls._add_cache_key_to_refresh(extra_args)
    if len(cache_key) >= 250:
        m = hashlib.md5()
        m.update(cache_key)
        cache_key = m.hexdigest()
    return cache_key, cache.get(cache_key)


def cached_label_changed(sender, **kwargs):
    if not kwargs.get('instance'):
        return
    instance = kwargs.get('instance')
    lbl = instance._generate_cached_label()
    if lbl != instance.cached_label:
        instance.cached_label = lbl
        instance.save()

SHORTIFY_STR = ugettext(" (...)")


def shortify(lbl, number=20):
    if len(lbl) <= number:
        return lbl
    return lbl[:number - len(SHORTIFY_STR)] + SHORTIFY_STR


def mode(array):
    most = max(list(map(array.count, array)))
    return list(set(filter(lambda x: array.count(x) == most, array)))


def _get_image_link(item):
    # manage missing images
    if not item.thumbnail or not item.thumbnail.url:
        return ""
    return mark_safe(u"""
    <div class="welcome-image">
        <img src="{}"/><br/>
        <em>{} - {}</em>
        <a href="#" onclick="load_window(\'{}\')">
          <i class="fa fa-info-circle" aria-hidden="true"></i>
        </a>
        <a href="." title="{}">
            <i class="fa fa-random" aria-hidden="true"></i>
        </a><br/>
    </div>""".format(
        item.thumbnail.url,
        unicode(item.__class__._meta.verbose_name),
        unicode(item),
        reverse(item.SHOW_URL, args=[item.pk, '']),
        unicode(_(u"Load another random image?"))))


def get_random_item_image_link(request):
    from archaeological_operations.models import Operation
    from archaeological_context_records.models import ContextRecord
    from archaeological_finds.models import Find

    ope_image_nb, cr_image_nb, find_image_nb = 0, 0, 0
    if request.user.has_perm('archaeological_operations.view_operation',
                             Operation):
        ope_image_nb = Operation.objects.filter(
            thumbnail__isnull=False).count()
    if request.user.has_perm(
            'archaeological_context_records.view_contextrecord',
            ContextRecord):
        cr_image_nb = ContextRecord.objects.filter(
            thumbnail__isnull=False).count()
    if request.user.has_perm('archaeological_finds.view_find',
                             Find):
        find_image_nb = Find.objects.filter(
            thumbnail__isnull=False).count()

    image_total = ope_image_nb + cr_image_nb + find_image_nb
    if not image_total:
        return ''

    image_nb = random.randint(0, image_total - 1)
    if image_nb >= 0 and image_nb < ope_image_nb:
        return _get_image_link(
            Operation.objects.filter(thumbnail__isnull=False).all()[image_nb])
    if image_nb >= ope_image_nb and image_nb < (cr_image_nb + ope_image_nb):
        return _get_image_link(
            ContextRecord.objects.filter(thumbnail__isnull=False).all()[
                image_nb - ope_image_nb])
    if image_nb >= (cr_image_nb + ope_image_nb):
        return _get_image_link(
            Find.objects.filter(thumbnail__isnull=False).all()[
                image_nb - ope_image_nb - cr_image_nb])
    # should never happen except in case of deletion during the excution
    return ''
