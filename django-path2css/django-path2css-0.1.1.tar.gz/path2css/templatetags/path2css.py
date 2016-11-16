# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import template
from path2css import request_path_to_css_names, Output
register = template.Library()

@register.simple_tag(takes_context=False)
def path2css(path, prefix='', suffix='', midpoint='-'):
    variations = request_path_to_css_names(item=path, prefix=prefix, suffix=suffix,
                                           midpoint=midpoint)
    return Output(variations)
