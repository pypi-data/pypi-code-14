from __future__ import absolute_import

from lazy_serializer.base import Serializer
from lazy_serializer import fields
from sqlalchemy import types

try:
    from sqlalchemy_utils import JSONType, ScalarListType
except ImportError:
    class ScalarListType(object):
        pass

    class JSONType(object):
        pass


SERIALIZER_FIELD_MAPPING = {
    types.Integer: fields.IntegerField,  # -> SmallInteger, BigInteger
    types.Boolean: fields.BooleanField,  # -> MatchType
    types.Date: fields.DateField,
    types.DateTime: fields.DateTimeField,
    types.Time: fields.TimeField,
    types.String: fields.StringField,  # -> Enum
    types.Numeric: fields.FloatField,  # -> Float
    ScalarListType: lambda: fields.ListField(fields.StringField),
    JSONType: fields.DictField,
    # types.Interval: not implemented
    # types.LargeBinary: not implemented
    # types.PickleType: not implemented
    # types.SchemaType: not implemented
}


add_type_mapping = SERIALIZER_FIELD_MAPPING.__setitem__


class ModelSerializer(Serializer):
    def __init__(self):
        super(ModelSerializer, self).__init__()

        self._table = self.options.model
        if hasattr(self._table, "__table__"):
            self._table = self._table.__table__

        field_names = [f.name for f in self.fields]

        auto_fields = False
        if not hasattr(self.options, "fields"):
            self.options.fields = self._table.columns.keys()
            auto_fields = True

        for name in self.options.fields:
            if name in field_names:
                continue

            column = self._table.columns[name]

            for t, f in SERIALIZER_FIELD_MAPPING.items():
                if isinstance(column.type, t):
                    field = f()
                    field.name = name
                    field.object_field_name = name
                    self.fields.append(field)
                    break
            else:
                if not auto_fields:
                    raise NotImplementedError(
                        "%r type is not supported" % column.type)
