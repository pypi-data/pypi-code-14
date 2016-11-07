from django import template

register = template.Library()

@register.simple_tag
def replace(s, old, new, maxreplace = None):
    return s.replace(old, new, maxreplace)
