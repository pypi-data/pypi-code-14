# -*- coding:utf-8 -*-
from sqlalchemy_wrapper import BaseQuery


class PalvinQuery(BaseQuery):

    def with_entity(self, field):
        return [instance[0] for instance in self.with_entities(field)]

    def join_with_entities(self, attr):
        return self.join(attr).with_entities(attr.mapper.class_)
