from qubit.io.postgres import types
from qubit.io.postgres import QuerySet

__all__ = ['Mapper']

mapper_table = types.Table('mapper', [
    ('name', types.varchar),
    ('side_effect', types.boolean),
    ('closure', types.json),
    ('body', types.text)
])


class Mapper(object):
    manager = QuerySet(mapper_table)

    @classmethod
    def create(cls, name, body, closure={}, side_effect=0):
        return cls.manager.insert(name=name,
                                  body=body,
                                  closure=closure,
                                  side_effect=side_effect)

    @classmethod
    def get_raw(cls, mid):
        return cls.manager.get(mid)

    @staticmethod
    def load_mapper(mapper: dict):
        pass

    @classmethod
    def delete(cls, mid):
        return cls.mapper.delete(id=mid)
