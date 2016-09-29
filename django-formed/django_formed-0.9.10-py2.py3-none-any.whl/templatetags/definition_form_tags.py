# coding=utf-8
from __future__ import unicode_literals
from django import template
from formed import settings as formed_settings
from formed.form_elements import page_elements_from_definition

register = template.Library()

@register.assignment_tag(takes_context=True)
def field_value(context, name, data=None):
    form_definition = context.get('form_definition')
    if data is None:
        session_data = context['request'].session.get(formed_settings.FORMED_SESSION_NAME)
        if session_data is not None:
            data = session_data.get(form_definition.get_session_key())
    if data is not None and name in data:
        # todo: This returns the value, even for multi-valued fields. We should have a way to return the display value.
        return data[name]
    return ''

@register.assignment_tag()
def definition_pages(form_definition, form=None):
    pages = []
    for page_index in range(form_definition.page_count()):
        pages.append(page_elements_from_definition(form_definition, page_index=page_index, form=form))
    return pages
