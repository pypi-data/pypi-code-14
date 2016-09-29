# coding=utf-8
from formed import settings
from django.utils import six


def get_field_display_name(field_type):
    """
    Returns the display name for the field with the given field type.
    :param str field_type: The type of the field. For example 'CharField'.
    :return:
    """
    for field in six.itervalues(settings.FORMED_FORM_FIELDS):
        if field['type'] == field_type:
            return field['name']
    return None


def get_source_url_from_request(request):
    """
    Returns the Source url value from the given request. Override this if you use custom headers or if you wish to
    modify the result (strip query parameters, use only the path component etc.).
    :param django.http.HttpRequest request:
    :rtype: str
    """
    return request.META.get('HTTP_REFERER')


def import_attribute(module_path):
    """
    Imports the attribute defined by the given module_path.
    :param module_path: E.g. some.package.my_function
    :return:
    """
    import importlib
    module_name, attr = module_path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr)
