"""
Provides various utility functions and decorators.
"""
from functools import wraps
from inspect import cleandoc

from jsonschema import (validate as jsonschema_validate,
                        ValidationError as JsonSchemaValidationError,
                        FormatChecker)

from untt.ex import ValidationError


def parse_docstring(doc):
    """
    Parses title and description out of a docstring.
    """
    doc_split = cleandoc(doc).split('\n')
    if len(doc_split) == 1:
        return doc_split[0], ''
    elif doc_split[1] != '':
        return '', '\n'.join(doc_split)
    else:
        title = doc_split[0]
        description = '\n'.join(doc_split[2:])

        return title, description


def entity_base(klass):
    """
    Indicates that an `Entity` is a base and not an actual one.

    Entities decorated with this decorator will not be included in the root
    schema definitions.
    """
    del klass.schema_definitions[klass.__name__]
    return klass


@wraps(jsonschema_validate)
def validate(*args, **kwargs):
    """
    jsonschema.validate wrapper, that raises `untt.ex.ValidationError`.
    """
    try:
        jsonschema_validate(*args, **kwargs, format_checker=FormatChecker())
    except JsonSchemaValidationError as ex:
        raise ValidationError(str(ex)) from ex


class EmptyValue(object):  # pragma: nocover
    """Used to represent an empty dummy value."""
    pass
