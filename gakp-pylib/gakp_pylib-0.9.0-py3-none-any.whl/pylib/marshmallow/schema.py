from marshmallow import Schema
from marshmallow.fields import Int
from pylib.lib import now
from pylib.marshmallow.fields import ObjectID, LagosDateTime


class BaseSchema(Schema):
    id = Int(dump_only=True)
    createdat = LagosDateTime(missing=now)


class MongoSchema(Schema):
    id = ObjectID(dump_only=True)
    _id = ObjectID(dump_to='id', dump_only=True)
    createdat = LagosDateTime(missing=now)
