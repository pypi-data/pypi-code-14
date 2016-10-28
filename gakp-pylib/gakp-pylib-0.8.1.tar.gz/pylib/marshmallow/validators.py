import re
from decimal import Decimal
from pyfunk.combinators import curry, compose


def __decimal_tuple(num):
    return Decimal(str(num)).as_tuple()


def __validate_decimal(size, places, d):
    return abs(d.exponent) <= places and len(d.digits) <= size


@curry
def float_check(size, places):
    """
    Creates a function for validating floats as decimals. It checks
    wether the float as `size` digits and is in `places` places
    @sig float_validator :: Int -> Int -> (Float -> Bool)
    """
    return compose(__validate_decimal(size, places), __decimal_tuple)


def enum(*options):
    """
    Creates a validator for enumerations
    @sig enum :: * -> (a -> Bool)
    """
    return lambda v: v in options

sex_check = enum('Male', 'Female')
title_check = enum('Mr', 'Mrs', 'Dr', 'Miss', 'Master')
maritalstatus_check = enum('Single', 'Married', 'Divorced')
religion_check = enum('Christianity', 'Islam', 'Other')

fullname_check = lambda x: len(x.split(' ')) >= 2  # noqa

phonereg = re.compile(r'^\+(?:[0-9] ?){6,14}[0-9]$')
phoneno_check = lambda x: bool(phonereg.match(x))  # noqa
