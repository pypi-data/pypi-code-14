from qubit.io.postgres import types
from qubit.io.postgres import QuerySet
from qubit.types.function import Function

__all__ = ['Mapper']


class Mapper(Function):
    prototype = types.Table('mapper', [
        ('id', types.integer),
        ('name', types.varchar),
        ('side_effect', types.boolean),
        ('closure', types.json),
        ('body', types.text)
    ])
    manager = QuerySet(prototype)
