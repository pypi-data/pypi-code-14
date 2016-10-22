# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import csv


class Parser(object):
    fields_order = []

    def __init__(self):
        self.errors = None

    @classmethod
    def parse_file(cls, file_path, start_from_line=1, csv_reader=csv.reader, **kwargs):
        return cls.parse_file_object(open(file_path, 'r'), start_from_line, csv_reader, **kwargs)

    @classmethod
    def parse_file_object(cls, file_object, start_from_line=1, csv_reader=csv.reader, **kwargs):
        cls.check_if_fields_order_contains_proper_names()

        with file_object as file:
            reader = csv_reader(file, **kwargs)
            fields = cls.get_all_field_names_declared_by_user()

            for skipped_row in range(1, start_from_line):
                next(reader)

            for line_num, row in enumerate(reader, start=start_from_line):
                instance = cls()
                for i, field in enumerate(fields):
                    setattr(instance, field, row[i])
                yield instance

    @classmethod
    def get_all_field_names_declared_by_user(cls):
        if not cls.fields_order:
            raise RuntimeError('You have to specify fields_order')

        return cls.fields_order

    def is_valid(self):
        """
        Validates single instance. Returns boolean value and store errors in self.errors
        """
        self.errors = []

        for field in self.get_all_field_names_declared_by_user():
            getattr(type(self), field).is_valid(self, type(self), field)
            field_errors = getattr(type(self), field).errors(self)
            self.errors.extend(field_errors)

        return len(self.errors) == 0

    @classmethod
    def check_if_fields_order_contains_proper_names(cls):
        for field in cls.fields_order:
            if not hasattr(cls, field):
                raise ValueError('fields_order has {field_name}, but {field_name} is not defined on Parser.'.format(field_name=field))

        return True

    def __iter__(self):
        for field in self.get_all_field_names_declared_by_user():
            yield getattr(self, field)