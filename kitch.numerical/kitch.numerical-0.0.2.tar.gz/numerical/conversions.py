"""
This module contains numerical conversions.
"""

import decimal

import numerical.predicates as predicates

__all__ = ['to_dec']


def to_dec(x):
    """If the given object is a number, convert it to a decimal number."""
    return decimal.Decimal(str(x)) if predicates.is_num(x) else x
