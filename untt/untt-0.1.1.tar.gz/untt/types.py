"""
Defines primitive field types
"""
import datetime

import iso8601

from untt.field import Field
from untt import util
from untt.ex import DefinitionError

from untt.util import EmptyValue


class PrimitiveType(Field):
    """
    A Field type that represents a primitive type, defined by JSON Schema.
    """
    _ACCEPTABLE_TYPES = ('string', 'boolean', 'integer',
                         'number', 'null', 'array')
    empty = EmptyValue()

    def __init__(self, property_type, *,
                 title="", description="",
                 default=empty, nullable=False,
                 **keywords):
        if property_type not in self._ACCEPTABLE_TYPES:
            raise DefinitionError(
                "A property must be of one of the following types: %s",
                self._ACCEPTABLE_TYPES
            )

        self.property_type = property_type
        self.default = default
        self.keywords = keywords

        super(PrimitiveType, self).__init__(title=title,
                                            description=description,
                                            optional=default is not self.empty,
                                            nullable=nullable)

    @property
    def json_schema(self):
        """
        The JSON Schema definition for the primitive type.
        """
        schema = {
            'type': self.property_type,

            'title': self.title,
            'description': self.description,

            **self.keywords
        }

        if self.default is not self.empty:
            schema['default'] = self.default

        if self.nullable:
            schema = {
                'oneOf': [
                    schema,
                    {'type': 'null'}
                ]
            }

        return schema

    def _validate(self, json_value):
        util.validate(json_value, self.json_schema)


class BaseType(PrimitiveType):
    """
    Base class for easy primitive type definition.
    """
    property_type = None
    keywords = {}

    def __init__(self, *, title="", description="",
                 default=PrimitiveType.empty, nullable=False,
                 **keywords):
        self.keywords.update(keywords)
        super(BaseType, self).__init__(self.property_type, title=title,
                                       description=description,
                                       nullable=nullable, default=default,
                                       **self.keywords)


class Integer(BaseType):
    """
    JSON Schema integer type.
    """
    property_type = 'integer'


class Number(BaseType):
    """
    JSON Schema number type.
    """
    property_type = 'number'


class String(BaseType):
    """
    JSON Schema string type.
    """
    property_type = 'string'


class Array(BaseType):
    """
    JSON Schema array type.
    """
    property_type = 'array'
    keywords = {
        'items': {}
    }


class Boolean(BaseType):
    """
    JSON Schema boolean type.
    """
    property_type = 'boolean'


class Datetime(String):
    """
    JSON Schema string type with date-time format.

    This accepts a `datetime` Python object as a value and converts back and
    forth automatically.
    """
    _python_type = datetime.datetime
    keywords = {
        'format': 'date-time'
    }

    def to_json(self, value):
        return value.isoformat()

    def from_json(self, json_value):
        return iso8601.parse_date(json_value)


class Email(String):
    """
    JSON Schema string type with email format.
    """
    keywords = {
        'format': 'email'
    }
