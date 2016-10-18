from congo.templatetags import Library
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.core.urlresolvers import reverse, NoReverseMatch

register = Library()

@register.filter
def admin_change_url(value):
#    {% url 'admin:index' %}
#    {% url 'admin:polls_choice_add' %}
#    {% url 'admin:polls_choice_change' choice.id %}
#    {% url 'admin:polls_choice_changelist' %}

    url = ""
    try:
        url = reverse('admin:%s_%s_change' % (value._meta.app_label, value._meta.model_name), args = (value.id,))
    except (NoReverseMatch, AttributeError):
        pass
    return url

@register.filter
def content_type_id(value):
    try:
        content_type = ContentType.objects.get_for_model(value)
        return content_type.id
    except AttributeError:
        return None

@register.filter
def class_name(obj):
    return obj.__class__.__name__

@register.filter
def module_class_name(obj):
    return "%s.%s" % (obj.__class__.__module__, obj.__class__.__name__)

@register.filter
def field_name(model, field):
    try:
        return model._meta.get_field(field).verbose_name
    except (FieldDoesNotExist, AttributeError):
        return field.title()
