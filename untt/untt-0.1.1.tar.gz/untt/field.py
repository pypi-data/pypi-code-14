"""
This module defines the root classes to implement entity fields.
"""
from untt.ex import ValidationError


class Field(object):
    """
    This is the root class for defining Entity fields.

    This implements the Descriptor protocol, and manages the values of the
    properties by validating the values being assigned to them. A subclasse
    should implement the `_validate` method for that.

    This class also provides the ability to convert other non-primitive types
    from and to JSON that are originally not serializable. To enable this onc
    may first specify the `_python_type` they expect. If specified, an
    additional instance type check will be performed. Next, the methods
    `from_json` and `to_json` methods should be extended.
    """
    _python_type = None

    def __init__(self, *, title="",
                 description="",
                 optional=False,
                 nullable=False):
        self.title = title
        self.description = description
        self.optional = optional
        self.nullable = nullable

        self._values = {}

    def __get__(self, owner, klass=None):
        if owner is None:
            return self
        else:
            return self._values[owner]

    def __set__(self, obj, value):
        if self._python_type:
            if not isinstance(value, self._python_type):
                raise ValidationError(
                    "'{}' is not a '{}' object".format(
                        value, self._python_type
                    )
                )

        json_value = self.to_json(value)
        self._validate(json_value)

        self._values[obj] = value

    def _validate(self, json_value):
        """
        Should raise ValidationError if `json_value` does not fit the shcema.
        """
        raise NotImplementedError()  # pragma: no cover

    def from_json(self, json_value):
        """
        Convert `json_value` to appropriate type.
        """
        return json_value

    def to_json(self, value):
        """
        Convert the `value` to JSON.
        """
        return value


class EntityField(Field):
    """
    A Field type that represents an `Entity` implementation.
    """
    def __init__(self, entity_type, *,
                 title="",
                 description="",
                 optional=False,
                 nullable=False):
        self.entity_type = entity_type
        self._python_type = entity_type

        super(EntityField, self).__init__(title=title,
                                          description=description,
                                          optional=optional,
                                          nullable=nullable)

    @property
    def json_schema(self):
        """
        The JSON schema definition for the field, i.e. entity.
        """
        return self.entity_type.entity_schema

    def from_json(self, json_value):
        return self.entity_type.from_json(json_value)

    def to_json(self, value):
        return value.to_json()

    def _validate(self, json_value):
        self.entity_type.validate(json_value)
