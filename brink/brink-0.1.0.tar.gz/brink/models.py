from inflection import tableize
from cerberus import Validator
from brink.db import conn
from brink.object_manager import ObjectManager
from brink.exceptions import UndefinedSchema, UnexpectedDbResponse, ValidationError
import rethinkdb as r


class MetaModel(type):

    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        table_name = tableize(name)
        setattr(new_cls, "objects", ObjectManager(new_cls, table_name))
        setattr(new_cls, "table_name", table_name)
        return new_cls

    def __getattr__(self, attr):
        return getattr(self.objects, attr)


class Model(object, metaclass=MetaModel):

    schema = None
    data = {}

    def __init__(self, **kwargs):
        self.data = kwargs

    def validate(self):
        if self.schema is None:
            raise UndefinedSchema()

        v = Validator(self.schema)

        if not v.validate(self.data):
            raise ValidationError(v.errors)

        return True

    async def save(self):
        if hasattr(self, 'before_save'):
            self.before_save()

        query = r.table(self.table_name)

        try:
            query = query.get(self.id).replace(self.data, return_changes=True)
        except AttributeError:
            query = query.insert(self.data, return_changes=True)

        resp = await query.run(await conn.get())

        try:
            changes = resp["changes"]

            if len(changes) > 0:
                self.replace(resp['changes'][0]['new_val'])
        except KeyError:
            raise UnexpectedDbResponse()

        return self

    async def delete(self):
        self.__class__.delete(self.id)

    def patch(self, data):
        if isinstance(data, Model):
            data = data.data

        self.data.update(data)
        return self

    def replace(self, data):
        self.data = {}
        return self.patch(data)

    def __getattr__(self, attr):
        try:
            return self.data[attr]
        except KeyError as e:
            raise AttributeError(attr)

    def __delattr__(self, attr):
        try:
            del self.data[attr]
        except KeyError:
            raise AttributeError(attr)

    def __getitem__(self, attr):
        return self.data[attr]

    def __setitem__(self, attr, value):
        self.data[attr] = value

    def __delitem__(self, attr):
        del self.data[attr]

    def __json__(self):
        return self.data

