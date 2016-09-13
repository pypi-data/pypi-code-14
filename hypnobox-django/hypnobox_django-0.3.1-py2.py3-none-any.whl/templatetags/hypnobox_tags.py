# coding: utf-8
from __future__ import unicode_literals

from django import template
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.template.loader import render_to_string

from ..models import Lead

register = template.Library()


@register.simple_tag(takes_context=True)
def new_lead(context, product_id, media='', template='hypnobox/_link.html'):
    link = reverse('{}:new_lead'.format(Lead._meta.app_label))
    params = urlencode(dict(product_id=product_id, media=media))
    context = {
        'url': "{}?{}".format(link, params),
    }
    return render_to_string(template, context)
