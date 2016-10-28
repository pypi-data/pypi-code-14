from pylib.marshmallow.fields import LagosDateTime, ObjectID
from pylib.marshmallow.schema import BaseSchema, MongoSchema
from pylib.marshmallow.serialize import load, dump
from pylib.marshmallow.validators import (
    enum,
    float_check as vfloat,
    sex_check as vsex,
    title_check as vtitle,
    maritalstatus_check as vmarriage,
    religion_check as vreligion,
    fullname_check as vfullname,
    phoneno_check as vphone
)
