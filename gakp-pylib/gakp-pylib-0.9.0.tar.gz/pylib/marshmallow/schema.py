import marshmallow
from marshmallow import fields

from pylib import lib
from pylib.marshmallow import fields as pyfields


class BaseSchema(marshmallow.Schema):
    id = fields.Int(dump_only=True)
    createdat = pyfields.LagosDateTime(missing=lib.now)


class MongoSchema(marshmallow.Schema):
    id = pyfields.ObjectID(dump_only=True)
    _id = pyfields.ObjectID(dump_to='id', dump_only=True)
    createdat = pyfields.LagosDateTime(missing=lib.now)
