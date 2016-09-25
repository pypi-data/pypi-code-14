import operator
import decimal


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