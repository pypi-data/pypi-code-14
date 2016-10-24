from django import template
from tag_manager.utils import resolve_tag

register = template.Library()


@register.inclusion_tag('tag_manager/include_tag.html', takes_context=True)
def tag_manager(context):
    context.update({
        'matching_tags': resolve_tag(context)})
    return context
