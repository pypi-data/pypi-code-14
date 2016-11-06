# coding: utf-8
from django import template

__author__ = 'mhaze'

register = template.Library()


@register.inclusion_tag('textflow.html')
def textflow(texts=None):
    if not isinstance(texts, str):
        raise Exception("Texts must be of type str")

    return {
        'texts': texts
    }
