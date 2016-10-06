import decimal
import datetime


class ParserField(object):
    fields_counter = 0

    def __init__(self, validators=None, null_symbols=None):
        if validators is None:
            self.validators = []
        else:
            self.validators = validators

        self.null_symbols = null_symbols
        self.name = None
        self.init_done = False
        self.name = '_parser_field' + str(ParserField.fields_counter)
        self.errors_field_name = '_parser_field_errors' + str(ParserField.fields_counter)
        ParserField.fields_counter += 1

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            raw_value = getattr(instance, self.name)

            if self.null_symbols is not None and raw_value in self.null_symbols:
                return None
            else:
                return self.create_real_value(raw_value)

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

    def create_real_value(self, raw_value):
        pass


class CharField(ParserField):
    def create_real_value(self, raw_value):
        return raw_value


class DecimalField(ParserField):
    def create_real_value(self, raw_value):
        return decimal.Decimal(raw_value)


class IntegerField(ParserField):
    def create_real_value(self, raw_value):
        return int(raw_value)


class DateField(ParserField):
    def __init__(self, date_format, **kwargs):
        super(DateField, self).__init__(**kwargs)
        self.date_format = date_format

    def create_real_value(self, raw_value):
        return datetime.datetime.strptime(raw_value, self.date_format)