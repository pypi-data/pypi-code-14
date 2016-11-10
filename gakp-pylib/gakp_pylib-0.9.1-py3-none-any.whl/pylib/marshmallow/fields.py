import bson
from bson import errors
import pytz

from marshmallow import fields


class ZonedDateTime(fields.Field):
    """
    This is a marshmallow field for managing datetime
    based on timezones. The main feature about this field
    is that it never deserializes. This prevents using datetime
    from unknown timezones and enforces usage of global utc timezone
    in iso format.
    """
    default_error_messages = {
        'invalidop': 'Deserialization is not allowed on this field',
        'invalid': 'Default value is not a valid date',
        'format': '"{input}" cannot be formatted as a datetime.',
        'utc': '"{input}" must be naive UTC timestamp'
    }
    locality = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.missing:
            self.dump_only = True

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        try:
            value = self.locality.localize(value)
            return value.isoformat()
        except AttributeError:
            self.fail('format', input=value)
        except ValueError:
            self.fail('utc', input=value)

    def _deserialize(self, value, attr, data):
        if self.missing:
            if callable(self.missing):
                return self.missing()
            else:
                return self.missing
        self.fail('invalidop')


class LagosDateTime(ZonedDateTime):
    locality = pytz.timezone('Africa/Lagos')


class ObjectID(fields.Field):
    """Serializes and deserializes ObjectId strs from mongodb"""
    default_error_messages = {
        'invalid': 'Not a valid ObjectId.',
        'format': '"{input}" cannot be formatted as an ObjectId.',
    }

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        elif isinstance(value, bson.ObjectId):
            return str(value)
        else:
            self.fail('format', input=value)

    def _deserialize(self, value, attr, obj):
        if not value:
            self.fail('invalid')
        try:
            return bson.ObjectId(value)
        except errors.InvalidId:
            self.fail('invalid')
