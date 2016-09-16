# -*- coding: utf-8 -*-

from future.moves.urllib.parse import urlparse

from ..html.root.attributes import TAG_ATTRIBUTES
from ..html.root.tags import TAGS


def validate_tag(tag=None):
    """Validates whether the given tag is supported by korona or not."""
    if not tag:
        raise AttributeError('Tag cannot be empty')

    if tag not in TAGS:
        raise ValueError('{0} tag is not supported')


def validate_tag_attribute_value(tag, value):
    """Validates whether the given value is a string or not."""
    if not value:
        return

    # If the attribute value is not a string raise a ValueError.
    if not isinstance(value, str):
        raise ValueError('<{tag}>: {value} should be a string'
                         .format(tag=tag, value=value))


def validate_attribute_values(tag, attribute_name, value):
    """Validates whether the given attribute value is a valid value or not.
    Some of the attributes have confined values. Even if we give some
    other value, the html output would not be correct.
    """
    if not value:
        return

    if not isinstance(value, str):
        raise ValueError('<{tag}>: {attribute} should be a string value.'
                         .format(tag=tag, attribute=attribute_name))

    attribute_values = TAG_ATTRIBUTES[tag][attribute_name]['values']

    if value not in attribute_values:
        raise AttributeError('<{tag}>: {attribute_name} attribute '
                             'values should be one of these: {values}'
                             .format(tag=tag,
                                     attribute_name=attribute_name,
                                     values=','.join(attribute_values)))


def validate_url(attribute_name, url):
    """Validates whether the given string is a URL or not."""
    if not url:
        return

    try:
        result = urlparse(url=url)
        if [result.scheme, result.netloc, result.path]:
            return True
    except:
        raise ValueError('{attribute_name}: The given string {url} is not a '
                         'valid url.'
                         .format(attribute_name=attribute_name, url=url))
