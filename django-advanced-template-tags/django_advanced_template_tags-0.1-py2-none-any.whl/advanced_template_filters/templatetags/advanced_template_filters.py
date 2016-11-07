from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def replace(s, old, new, maxreplace = None):
    return s.replace(old, new, maxreplace)
