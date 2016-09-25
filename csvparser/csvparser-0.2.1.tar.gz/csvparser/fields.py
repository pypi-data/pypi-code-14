import decimal


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


class CharField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return raw_value


class DecimalField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return decimal.Decimal(raw_value)


class IntegerField(ParserField):
    @staticmethod
    def create_real_value(raw_value):
        return int(raw_value)