"""
Defines classes for main entity functionality.
"""
from untt import util
from untt.field import Field, EntityField
from untt.util import entity_base, EmptyValue


SCHEMA_URL = 'http://json-schema.org/draft-04/schema#'


class EntityMeta(type):
    """
    The Entity metaclass that defines Entity type creation.

    This scans through the Fields of the Entity class and make appropriate
    setup for further use by the Entity class.
    """
    def __init__(cls, name, bases, dct):
        super(EntityMeta, cls).__init__(name, bases, dct)

        cls.untt_properties = cls._collect_untt_properties(bases, dct)

        title, description = util.parse_docstring(cls.__doc__ or '')
        cls.entity_schema = {
            'type': 'object',
            'properties': {
                n: p.json_schema for n, p in cls.untt_properties.items()
            },
            'required': [n for n, p in cls.untt_properties.items() if not
                         p.optional],
            'title': title,
            'description': description
        }

        if dct.get('schema_root', False):
            cls.schema_definitions = {}

        cls.schema_definitions[cls.__name__] = cls.entity_schema

    @property
    def json_schema(cls):
        """
        Returns the relative reference to the definition ofi its JSON Schema.
        """
        return {
            '$ref': '#/definitions/{}'.format(cls.__name__)
        }

    @classmethod
    def _collect_untt_properties(mcs, bases, dct):
        """
        Prepares a map of Fields defined for the Entity.
        """
        untt_properties = {}

        for base in bases:
            if isinstance(base, EntityMeta):
                untt_properties.update(base.untt_properties)

        untt_properties.update({
            name: p for name, p in dct.items()
            if isinstance(p, Field)
        })

        return untt_properties


@entity_base
class Entity(object, metaclass=EntityMeta):
    """
    Entity is the main class of untt.

    To define an entity users should subclass Entity and define its fileds
    using the provided types in `untt.types`, e.g.:

        class MyEntity(Entity):
            my_int_field = Integer()
            my-str_field = String()

    The JSON schema of the entity will be accessable as
    `MyEntity.entity_schema`. All the JSON schemas of the entities subclassing
    the `Entity` will be accessible via `Entity.schema_definitions`.

    When defining a base class for other entities, you may decorate it with the
    `untt.util.entity_base` to exclude it from all definitions. Also, to make
    a base class the root of shcema definitions and start from scratch, assign
    the class variable `schema_root` of the base class the value `True`.

    In order to define any field of the entity as another entity type, you may
    use the `as_property` class method, e.g.:

        class MyOtherEntity(Entity):
            my_entity_field = MyEntity.as_property()

    Finally, you will get a bonus functions `to_json` and `from_json` to
    convert your entity objects to/from JSON.
    """
    schema_root = True
    untt_properties = {}
    schema_definitions = {}
    entity_schema = {}
    json_schema = {}
    not_provided = EmptyValue()

    def to_json(self):
        """
        Convert `Entity` object to JSON object.
        """
        json_value = {}
        for name, prop in self.untt_properties.items():
            value = getattr(self, name)
            json_value[name] = prop.to_json(value)

        return json_value

    @classmethod
    def as_property(cls, *,
                    optional=False,
                    nullable=False):
        """
        Returns an `EntityField` instance representing the owning entity type.
        """
        return EntityField(cls,
                           optional=optional,
                           nullable=nullable)

    @classmethod
    def load_json(cls, json_obj):
        """
        Load a json object key-by-key.
        """
        cls.validate(json_obj)

        parsed_json_obj = {}
        for name, prop in cls.untt_properties.items():
            value = json_obj.get(name, cls.not_provided)

            if value is cls.not_provided and prop.default is not prop.empty:
                value = prop.default

            parsed_json_obj[name] = prop.from_json(value)

        return parsed_json_obj

    @classmethod
    def from_json(cls, json_value):
        """
        Initiate a `cls` instance out of a JSON object.
        """
        json_obj = cls.load_json(json_value)

        try:
            obj = cls()
        except TypeError as ex:
            raise TypeError(
                "'{}' implements a custom '__init__' with arguments. "
                "Please implement a custom 'from_json' to support it."
                .format(cls.__name__)
            ) from ex

        for name, value in json_obj.items():
            setattr(obj, name, value)

        return obj

    @classmethod
    def validate(cls, json_value):
        """
        Validate a given `json_value` against the `cls` JSON schema.
        """
        schema = {
            '$schema': SCHEMA_URL,
            'definitions': cls.schema_definitions,
        }
        schema.update(cls.json_schema)
        util.validate(json_value, schema)
