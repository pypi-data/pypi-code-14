# coding=utf-8
import importlib

from stdnumfield import STDNUM_FORMATS


def import_stdnum(num_format):
    """
    Returns Python module from stdnum package.
    Usage:
    >>> import_stdnum('damm')  #doctest: +ELLIPSIS
    <module 'stdnum.damm' from ...
    >>> import_stdnum('hr.oib')  #doctest: +ELLIPSIS
    <module 'stdnum.hr.oib' from ...
    """
    if num_format not in STDNUM_FORMATS:
        raise ValueError('Unknown stdnum format: "{}"'.format(num_format))
    return importlib.import_module('stdnum.{}'.format(num_format))
