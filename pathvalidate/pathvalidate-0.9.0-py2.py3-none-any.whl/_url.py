# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import re

import dataproperty

from ._error import InvalidCharError

"""
__RE_URL = re.compile("/^([:/?#[]@!$&'()*+,;=-._~a-zA-Z]|%[0-9a-fA-F]{2})+$")

#  :/?#[]@!$&'()*+,;=-._~


def validate_url(url):
    if dataproperty.is_empty_string(url):
        raise ValueError("url is empty")

    if __RE_URL.search(url) is None:
        raise InvalidCharError("invalid char found: url={:s}".format(url))
"""
