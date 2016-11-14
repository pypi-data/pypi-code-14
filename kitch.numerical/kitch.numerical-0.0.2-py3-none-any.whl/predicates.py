"""
This module contains numerical predicate functions.
"""

import decimal
import numbers

__all__ = ['is_num', 'all_num']


def is_num(x):
    """Is the given object a number?"""
    if isinstance(x, numbers.Real) and not isinstance(x, bool):
        return True
    if isinstance(x, decimal.Decimal):
        return True
    return False


def all_num(seq):
    """Are all the elements of the sequence numbers?"""
    return all(is_num(x) for x in seq)
