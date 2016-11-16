# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import enum
import inflection
from sqlalchemy_enum34 import EnumType
from sqlalchemy_wrapper import Model as BaseModel

from palvin.mixin import IdMixin, TimestampMixin, CRUDMixin


def make_palvin_model(declared_base):

    class PalvinModel(IdMixin, TimestampMixin, declared_base):
        __abstract__ = True

    return PalvinModel


class PalvinTableNameDescriptor(object):
    """
    Create the table name if it doesn't exist.
    """

    def __get__(self, obj, type):
        return inflection.tableize(type.__name__)


class PalvinBaseModel(CRUDMixin, BaseModel):

    def __iter__(self):
        """Returns an iterable that supports .next()
        so we can do dict(sa_instance).
        """
        for k in self.__dict__.keys():
            if not k.startswith('_'):
                yield (k, getattr(self, k))

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    @classmethod
    def flush(cls):
        cls.db.flsuh()

    @classmethod
    def commit(cls, callback=None):
        try:
            cls.db.commit()
            if hasattr(callback, '__call__'):
                callback()
        except Exception:
            cls.db.rollback()
            raise


class PlavinEnumType(EnumType):
    def process_result_value(self, value, dialect):
        if self._by_name:
            return self._enum_class[value] if value else None
        return self._enum_class.from_string(value) if value else None


class PalvinEnum(enum.Enum):
    __enumname__ = None

    """
    Typical usage::

        class Size(db.Enum):
            small = 's'
            medium = 'm'

        class Color(db.Enum):
            black = 'black', 2
            white = 'white', 1

        >>> Size.items()
        [('small', <Size.small: 's'[0]>), ('medium', <Size.medium: 'm'[0]>)]
        >>> Color.items()
        [('white', <Color.white: 'white'[1]>), ('black', <Color.black: 'black'[2]>)]
    """

    def __repr__(self):
        order = self.order
        if order is not None:
            return "<%s.%s: %r[%d]>" % (self.__class__.__name__, self._name_, self.value, order)
        return "<%s.%s: %r>" % (self.__class__.__name__, self._name_, self.value)

    def __str__(self):
        return "%s.%s" % (self.__class__.__name__, self._name_)

    @property
    def value(self):
        """The value of the Enum member."""
        if isinstance(self._value_, tuple):
            return self._value_[0]
        return self._value_

    @property
    def order(self):
        """The order of the Enum member."""
        if isinstance(self._value_, tuple) and len(self._value_) > 1:
            return self._value_[1]
        return 0

    @classmethod
    def from_string(cls, value, default=None):
        return getattr(cls, value) if hasattr(cls, value) else default

    @classmethod
    def items(cls):
        return sorted(cls.__members__.items(), key=lambda item: item[1].order)

    @classmethod
    def db_type(cls):
        name = cls.__enumname__ or inflection.tableize(cls.__name__)
        return PlavinEnumType(cls, name=name)
