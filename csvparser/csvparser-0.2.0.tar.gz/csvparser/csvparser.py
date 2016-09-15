# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import decimal
import operator


class Parser(object):
    fields_order = None

    def __init__(self):
        self.errors = None

    @classmethod
    def parse_file(cls, file_path, start_from_line=1, end_at_line=None,
                   csv_reader=csv.reader, **kwargs):

        with open(file_path, 'r') as file:
            reader = csv_reader(file, **kwargs)
            fields = cls.get_all_field_names_declared_by_user()

            for skipped_row in range(1, start_from_line):
                next(reader)

            for line_num, row in enumerate(reader, start=start_from_line):
                if end_at_line is not None and line_num > end_at_line:
                    break

                instance = cls()
                for i, field in enumerate(fields):
                    setattr(instance, field, row[i])
                yield instance

    @classmethod
    def get_all_field_names_declared_by_user(cls):
        return cls.fields_order

    def is_valid(self):
        self.errors = []

        for field in self.get_all_field_names_declared_by_user():
            getattr(type(self), field).is_valid(self, type(self), field)
            field_errors = getattr(type(self), field).errors(self)
            self.errors.extend(field_errors)

        return len(self.errors) == 0


class ParserField(object):
    fields_counter = 0

    def __init__(self, validators=None):
        if validators is None:
            self.validators = []
        else:
            self.validators = validators

        self.name = None
        self.init_done = False
        self.name = '_parser_field' + str(ParserField.fields_counter)
        self.errors_field_name = '_parser_field_errors' + str(ParserField.fields_counter)
        ParserField.fields_counter += 1

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return self.create_real_value(getattr(instance, self.name))

    def __set__(self, instance, value):
        setattr(instance, self.name, value)

    def is_valid(self, instance, cls, field_name):
        value = self.__get__(instance, cls)
        setattr(instance, self.errors_field_name, [])
        validation_results = []

        for validator in self.validators:
            field_is_valid = validator.is_valid(self.create_real_value(value), field_name)
            if not field_is_valid:
                current_errors = getattr(instance, self.errors_field_name)
                current_errors.extend(validator.errors)
            validation_results.append(field_is_valid)

        return all(validation_results)

    def errors(self, instance):
        return getattr(instance, self.errors_field_name)

    @staticmethod
    def create_real_value(raw_value):
        pass


class IntegerField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return int(raw_value)


class DecimalField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return decimal.Decimal(raw_value)


class CharField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return raw_value


class CompareValidator(object):
    def __init__(self, threshold, compare_operator, error_message_template):
        self.threshold = threshold
        self.errors = []
        self.compare_operator = compare_operator
        self.error_message_template = error_message_template

    def is_valid(self, validated_object, field_name):
        object_is_valid = self.apply_operator(validated_object)
        if object_is_valid:
            return True
        else:
            self.errors = [self.error_message_template.format(field_name=field_name)]
            return False

    def apply_operator(self, value):
        pass


class CharFieldLengthValidator(CompareValidator):
    def apply_operator(self, value):
        return self.compare_operator(len(value), self.threshold)


class CharFieldMaxLengthValidator(CharFieldLengthValidator):
    def __init__(self, max_length):
        super(CharFieldMaxLengthValidator, self).__init__(max_length, operator.le,
                                                          '{field_name} len higher than max_length')


class CharFieldMinLengthValidator(CharFieldLengthValidator):
    def __init__(self, min_length):
        super(CharFieldMinLengthValidator, self).__init__(min_length, operator.ge,
                                                          '{field_name} len smaller than min_length')


class NumericalFieldValueValidator(CompareValidator):
    def apply_operator(self, value):
        return self.compare_operator(value, self.threshold)


class IntegerFieldMaxValidator(NumericalFieldValueValidator):
    def __init__(self, max_value):
        super(IntegerFieldMaxValidator, self).__init__(max_value, operator.le,
                                                       '{field_name} higher than max')


class IntegerFieldMinValidator(NumericalFieldValueValidator):
    def __init__(self, min_value):
        super(IntegerFieldMinValidator, self).__init__(min_value, operator.ge,
                                                       '{field_name} lower than min')


class DecimalFieldMaxValidator(NumericalFieldValueValidator):
    def __init__(self, max_value):
        if not isinstance(max_value, decimal.Decimal):
            raise TypeError('max_value on DecimalFieldMaxValidator has to be decimal')

        super(DecimalFieldMaxValidator, self).__init__(max_value, operator.le,
                                                       '{field_name} higher than max_value')


class DecimalFieldMinValidator(NumericalFieldValueValidator):
    def __init__(self, min_value):
        if not isinstance(min_value, decimal.Decimal):
            raise TypeError('min_value on DecimalFieldMinValidator has to be decimal')

        super(DecimalFieldMinValidator, self).__init__(min_value, operator.ge,
                                                       '{field_name} lower than min_value')
