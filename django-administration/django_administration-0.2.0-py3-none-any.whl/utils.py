from django.utils.html import format_html
from django.utils.safestring import mark_safe


def foreign_link(cls, obj, attr, attr_name):
    """
    Displays FKs as 'admin:<app_label>_<model_name>_change' links.
    """
    from django.urls import reverse

    obj = attr
    link = reverse(
        'admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[str(obj.pk)])
    return mark_safe('<a href="{}">{}</a>'.format(link, obj))


def colored_name(cls, obj, attr, attr_name):
    """
    Displays field within a colored label.
    """
    mapping = {
        1: 'default',
        2: 'warning',
        3: 'info',
        4: 'success',
        5: 'danger',
    }
    return format_html(
        '<span class="label label-{}">{}</span>', mapping[getattr(obj, attr_name)],
        getattr(obj, 'get_%s_display' % attr_name)())
