# coding=utf-8
from __future__ import unicode_literals
from django.utils import six


def make_json_serializable(value):
    """
    Returns the given value as a JSON serializable value
    :param value:
    :rtype: int|float|bool|str|dict|None
    """
    if value is None or isinstance(value, (int, float, bool, six.text_type, dict)):
        return value
    return six.text_type(value)


def make_list_json_serializable(data):
    serializable = []
    for value in data:
        if isinstance(value, dict):
            value = make_dict_json_serializable(value)
        if isinstance(value, list):
            value = make_list_json_serializable(value)
        else:
            value = make_json_serializable(value)
        serializable.append(value)
    return serializable


def make_dict_json_serializable(data):
    """
    Makes the given dict JSON serializable.
    :param dict data:
    :return: The given dictionary but with the values safe for serializing.
    :rtype: dict
    """
    serializable = {}
    for key, value in data.items():
        if isinstance(value, dict):
            value = make_dict_json_serializable(value)
        if isinstance(value, list):
            value = make_list_json_serializable(value)
        else:
            value = make_json_serializable(value)
        serializable[key] = value
    return serializable
