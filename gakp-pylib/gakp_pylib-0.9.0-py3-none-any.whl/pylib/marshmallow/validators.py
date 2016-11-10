from decimal import Decimal
from marshmallow.validate import OneOf, Regexp, Validator
from pyfunk.combinators import compose


def __decimal_tuple(num):
    return Decimal(str(num)).as_tuple()


def __validate_decimal(size, places, d):
    return abs(d.exponent) <= places and len(d.digits) <= size


class FloatValidator(Validator):

    def __init__(self, size, places):
        if size <= places:
            raise ValueError('The size must be greater than the number of decimal place')
        self.__valid =  compose(__validate_decimal(size, places), __decimal_tuple)

    def __call__(self, num):
        return self.__valid(num)


validate_sex = OneOf(['Male', 'Female'])
validate_title = OneOf(['Mr', 'Mrs', 'Dr', 'Miss', 'Master'])
validate_maritalstatus = OneOf(['Single', 'Married', 'Divorced'])
validate_religion = OneOf(['Christianity', 'Islam', 'Other'])
validate_phoneno = Regexp(r'^\+(?:[0-9] ?){6,14}[0-9]$')
validate_fullname = lambda x: len(x.split(' ')) >= 2  # noqa
