# coding=utf-8
from __future__ import unicode_literals
from django import forms
from django.utils import html, six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.version import get_version
from distutils.version import StrictVersion

from formed import settings as formed_settings


def enforce_field_object(field_object):
    """
    Makes sure the given field 'object' is a dictionary containing required or easy to determine keys.
    :param basestring|dict field_object:
    :rtype: dict
    """
    if isinstance(field_object, six.string_types):
        # Create a new field object based on the given 'label'
        field = {
            'name': slugify(field_object),
            'label': field_object,
        }
    else:
        # Copy to make sure we don't modify the existing definition:
        field = field_object.copy()

    if 'type' not in field:
        field['type'] = formed_settings.FORMED_DEFINITION_DEFAULT_FIELD_TYPE

    if 'required' not in field:
        field['required'] = False

    if StrictVersion(get_version()) > StrictVersion('1.7') and \
            'label_suffix' not in field:

        if field['required'] and formed_settings.FORMED_FORM_REQUIRED_LABEL_SUFFIX is not None:
            # The required suffix:
            field['label_suffix'] = formed_settings.FORMED_FORM_REQUIRED_LABEL_SUFFIX
        elif not field['required'] and formed_settings.FORMED_FORM_OPTIONAL_LABEL_SUFFIX is not None:
            # The optional suffix:
            field['label_suffix'] = formed_settings.FORMED_FORM_OPTIONAL_LABEL_SUFFIX
        else:
            # The default suffix:
            field['label_suffix'] = formed_settings.FORMED_FORM_LABEL_SUFFIX

    return field


def get_field_class(class_name):
    """
    Returns the field class with the given name. Searches for the class in formed_settings.FORMED_FORM_FIELD_MODULES.
    :param str class_name:
    :rtype: django.forms.Field
    """
    for module in formed_settings.FORMED_FORM_FIELD_MODULES:
        if hasattr(module, class_name):
            return getattr(module, class_name)

    raise ImportError("No field class named '{name}' found in any modules defined in "
                      "'FORMED_FORM_FIELD_MODULES'".format(name=class_name))


def form_field_from_definition(field_definition):
    """
    Returns a form field instance for the given field definition
    :param dict field_definition: String with the field name or a dict field properties.
    :rtype: (str, forms.fields.Field)
    :return:
    """
    field_definition = enforce_field_object(field_definition)
    name = field_definition.pop('name', None)
    widget_arguments = {}

    assert name is not None, "Missing property 'name' in definition: {}".format(field_definition)

    field_class = get_field_class(field_definition.pop('type', formed_settings.FORMED_DEFINITION_DEFAULT_FIELD_TYPE))

    widget = field_definition.pop('widget', None)
    if widget is not None:
        field_definition['widget'] = getattr(forms, str(widget))
    elif not hasattr(field_class, 'widget') and 'choices' in field_definition:
        field_definition['widget'] = forms.Select

    attributes = field_definition.pop('widget_attributes', None)
    if attributes is not None:
        widget_arguments['attrs'] = {attr: value for attr, value in six.iteritems(attributes) if value is not None}
    if 'choices' in field_definition and not hasattr(field_class, 'choices'):
        # We got choices but the field does not accept them, the choices should be in the widget:
        widget_arguments['choices'] = field_definition.pop('choices')

    if 'widget' not in field_definition:
        # Default widget for the current field class:
        field_definition['widget'] = getattr(field_class, 'widget')

    # if widget_attributes:  # and isinstance(field_definition['widget'], forms.widgets.Widget):
    field_definition['widget'] = field_definition['widget'](**widget_arguments)

    return name, field_class(**field_definition)


def page_elements_from_definition(form_definition, page_index, form=None):
    return Page(form_definition.page(page_index=page_index), form)


@python_2_unicode_compatible
class Page(object):
    """
    Represents a single form page
    """
    name = None
    introduction = None
    fieldsets = None

    def __init__(self, page, form=None):
        self.name = page.get('name', None)
        self.introduction = page.get('introduction', None)
        assert 'fieldsets' in page, "Missing key 'fieldsets' in page"
        assert isinstance(page['fieldsets'], list), \
            "Property 'fieldsets' should be a list, {} given.".format(type(page['fieldsets']))
        # todo: can we make this lazy?
        self.fieldsets = [Fieldset(fieldset['rows'], form, legend=fieldset.get('legend', None)) for fieldset in
                          page['fieldsets']]

    def __iter__(self):
        return self.fieldsets.__iter__()

    def __str__(self):
        return html.mark_safe(''.join(six.text_type(fieldset) for fieldset in self.fieldsets))


@python_2_unicode_compatible
class Fieldset(object):
    """
    Represents a single form fieldset
    """
    rows = None
    legend = None

    def __init__(self, rows, form=None, legend=None):
        assert isinstance(rows, list), "Rows should be a list, {} given.".format(type(rows))
        # todo: can we make this lazy?
        self.rows = [Row(row, form) for row in rows]
        self.legend = legend

    def __iter__(self):
        return self.rows.__iter__()

    def __str__(self):
        rows_html = ''
        for row in self.rows:
            num_fields = len(row)
            rows_html += '<div class="form-row fields-{num_fields}{multiple_fields}">{row}</div>\n'.format(
                num_fields=num_fields,
                multiple_fields=' has-multiple-fields' if num_fields > 1 else '',
                row=six.text_type(row)
            )

        return '<fieldset class="fieldset rows-{num_rows}">{legend}\n{rows}</fieldset>'.format(
            num_rows=len(self.rows),
            legend='<legend class="legend">{}</legend>'.format(self.legend) if self.legend else '',
            rows=rows_html,
        )

    def __len__(self):
        return len(self.rows)


class Row(object):
    """
    Represents a single form row
    """
    fields = None

    def __init__(self, fields, form=None):
        assert isinstance(fields, list), "Rows should be a list, {} given.".format(type(fields))
        # todo: can we make this lazy?
        self.fields = [Field(field, form) for field in fields]

    def __iter__(self):
        return self.fields.__iter__()

    def __str__(self):
        """
        Returns all fields as their HTML representation.
        :return:
        """
        return html.mark_safe(''.join(six.text_type(field.as_html()) for field in self.fields))

    def __len__(self):
        return len(self.fields)


class Field(object):
    """
    Wrapper for a bound field to make sure the field is converted to a string properly.
    """
    field = None
    name = None

    def __init__(self, field, form=None):
        field = enforce_field_object(field)

        if form is not None and field['name'] in form.fields:
            self.name = field['name']
            self.field = form[field['name']]
        else:
            self.name, self.field = form_field_from_definition(field)

    def __str__(self):
        """
        As string we return the form field
        :return:
        """
        return six.text_type(self.field)

    def __getattr__(self, item):
        return getattr(self.field, item)

    def type(self):
        """
        To allow templates to check the type of a field.
        :return:
        """
        if hasattr(self.field, 'field'):
            return self.field.field.__class__.__name__
        else:
            return self.field.__class__.__name__

    def is_multi_valued(self):
        """
        Returns True when this field returns a list as value
        :return:
        """
        return type(self.field.to_python(None)) is list

    def is_boolean_valued(self):
        """
        Returns True when this field returns a boolean value
        :return:
        """
        return type(self.field.to_python(None)) is bool

    def as_html(self, tag='div', markup=None):
        """
        Returns the tag as proper markup
        :param basestring tag:
        :param basestring markup:
        :return:
        """
        if markup is None:
            markup = '<{tag} class="form-field{css_classes}">{label_tag} {field} {errors} {help_text}</{tag}>'
        items = {
            'tag': tag,
            'label_tag': self.field.label_tag(attrs={'class': 'label'}),
            'field': self.field.as_widget(attrs={'class': 'field'}),
            'css_classes': '',
            'help_text': '',
            'errors': self.field.errors
        }
        css_classes = self.field.css_classes()
        if css_classes:
            items['css_classes'] = ' {}'.format(css_classes)
        if not self.field.field.required:
            items['css_classes'] += ' {}'.format(formed_settings.FORMED_FORM_OPTIONAL_CSS_CLASS)
        if self.field.help_text:
            items['help_text'] = '<span class="help-text">{}</span>'.format(self.field.help_text)

        formatted = markup
        try:
            formatted = markup.format(**items)
        except KeyError:
            pass

        return html.mark_safe(formatted)

    def as_div(self):
        return self.as_html(tag='div')

    def as_span(self):
        return self.as_html(tag='span')
