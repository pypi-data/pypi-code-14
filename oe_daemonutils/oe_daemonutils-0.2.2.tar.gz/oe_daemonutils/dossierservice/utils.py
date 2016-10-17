# -*- coding: utf-8 -*-
import sys


# http://docs.pylonsproject.org/projects/pyramid/en/latest/_modules/pyramid/compat.html#text_
def text_(s, encoding='latin-1', errors='strict'):    # pragma: no cover
    """ If ``s`` is an instance of ``binary_type``, return
    ``s.decode(encoding, errors)``, otherwise return ``s``"""
    if sys.version_info[0] == 3:
        binary_type = bytes
    else:
        binary_type = str
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s
