# -*- coding:utf-8 -*-
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import UnmappedClassError

from sqlalchemy_wrapper import SQLAlchemy
from sqlalchemy_wrapper.helpers import _BoundDeclarativeMeta

from palvin.model import make_palvin_model, PalvinBaseModel, PalvinEnum
from palvin.query import PalvinQuery


class PalvinQueryProperty(object):
    def __init__(self, db):
        self.db = db

    def __get__(self, obj, type_):
        try:
            mapper = orm.class_mapper(type_)
            if mapper:
                return type_.query_cls(mapper, session=self.db.session())
        except UnmappedClassError:
            return None


class Palvin(SQLAlchemy):

    def __init__(self,
                 query_cls=PalvinQuery,
                 model_class=PalvinBaseModel,
                 store=None,
                 metaclass=None,
                 *args, **kwargs):
        super(Palvin, self).__init__(query_cls=query_cls, model_class=model_class, *args, **kwargs)

        self.BaseModel = self.make_declarative_base(model_class, metaclass=metaclass)
        self.BaseModel.db = self
        self.BaseModel.query = self.session.query
        self.BaseModel.query_cls = query_cls
        self.BaseModel.query_ = self.BaseModel.query
        self.BaseModel.query = PalvinQueryProperty(self)
        self.Model = make_palvin_model(declared_base=self.BaseModel)
        self.Enum = PalvinEnum
        self.store = store

    def make_declarative_base(self, model_class, metadata=None, metaclass=None):
        """Creates the declarative base."""
        return declarative_base(
            cls=model_class, name='Model',
            metadata=metadata, metaclass=metaclass if metaclass else _BoundDeclarativeMeta
        )
