# -*- coding: utf-8 -*-
"""
Utility functions for cable_modem_stats package

Created by phillip on 11/16/2016
"""

import re
from six import string_types

FLOAT_REGEX = re.compile(r'(-?[0-9]+(\.[0-9]+)?)')


def strip_float(string):
    if isinstance(string, string_types):
        string = FLOAT_REGEX.search(string).group(1)
    return float(string)
