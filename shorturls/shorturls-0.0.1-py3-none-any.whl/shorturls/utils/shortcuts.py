# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site

from ..models import Url


def get_shorturl(url=None, request=None):
    if not url:
        return None

    url_obj, _created = Url.objects.get_or_create(url=url)

    if request:
        current_site = get_current_site(request)
    else:
        current_site = Site.objects.get_current()
    return '{protocol}://{host}{url}'.format(
        protocol=getattr(settings, 'SHORTURLS_PROTOCOL', 'http'),
        host=current_site.domain,
        url=url_obj.get_short_url()
    )
