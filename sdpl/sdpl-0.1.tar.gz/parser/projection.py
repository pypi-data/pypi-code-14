__author__ = 'Bohdan Mushkevych'

import copy
from collections import Counter

from parser.relation import Relation
from schema.sdpl_schema import Schema, Field


def build_schema(*fields):
    schema = Schema()
    for field in fields:
        assert isinstance(field, Field)
        schema.fields.append(field)
    return schema


class FieldProjection(object):
    def __init__(self, schema_name:str, field_name:str, field:Field, as_field_name:str=None):
        self.schema_name = schema_name
        self.field_name = field_name
        self.as_field_name = as_field_name if as_field_name else field_name
        self.field = copy.deepcopy(field)

        # NOTICE: the schema.sdpl_schema.Field->name is changed here to `as_field_name`
        self.field.name = self.as_field_name

    def __str__(self):
        return '{0}.{1} AS {2}'.format(self.schema_name, self.field_name, self.as_field_name)

    @property
    def schema_field(self):
        return '{0}.{1}'.format(self.schema_name, self.field_name)


class RelationProjection(object):
    def __init__(self, relations):
        self.relations = relations

        # format list<FieldProjection>
        self.fields = list()
        self.fields_remove = list()

    def add_all(self, schema_name):
        schema = self.relations[schema_name].schema
        for f in schema.fields:
            self.add(schema_name, f.name)

    def remove_all(self, schema_name):
        schema = self.relations[schema_name].schema
        for f in schema.fields:
            self.remove(schema_name, f.name)

    def add(self, schema_name, field_name, as_field_name=None):
        schema = self.relations[schema_name].schema
        field_proj = FieldProjection(schema_name, field_name, schema[field_name], as_field_name)
        self.fields.append(field_proj)

    def remove(self, schema_name, field_name):
        schema = self.relations[schema_name].schema
        field_proj = FieldProjection(schema_name, field_name, schema[field_name])
        self.fields_remove.append(field_proj)

    def finalize_relation(self, relation_name):
        """ NOTICE: produced relation holds Fields with NAME replaced by AS_FIELD_NAME"""

        # Step 1: remove all the requested fields from `fields_add` collection

        # search criteria are different for *remove* and *duplicate search*
        # hence - resolve to manual indexing, rather than overriding FieldProjection.__eq__
        pop_indexes = set()
        schema_field_names = [f.schema_field for f in self.fields]
        for field_proj in self.fields_remove:
            try:
                index = schema_field_names.index(field_proj.schema_field)
                pop_indexes.add(index)
            except ValueError:
                print('WARNING: Referencing non-existent field {0} in *RelationProjection.finalize_relation*'
                      .format(field_proj.schema_field))

        # remove items from the tail of the list, so that the smaller indexes are still relevant
        pop_indexes = sorted(pop_indexes, reverse=True)
        for index in pop_indexes:
            self.fields.pop(index)

        # Step 2: Validate that the collection of the fields contains no duplicates

        # search criteria are different for *remove* and *duplicate search*
        # hence - resolve to manual indexing, rather than overriding FieldProjection.__eq__
        as_field_names = [f.as_field_name for f in self.fields]
        duplicates = [item for item, count in Counter(as_field_names).items() if count > 1]
        if duplicates:
            raise ValueError('fields {0} already present in the temporary schema'.format(sorted(duplicates)))

        # Step 3: build the schema and return it to the caller wrapped in Relation
        schema = build_schema(*[f.field for f in self.fields])
        relation = Relation(relation_name, None)
        relation._schema = schema
        return relation
