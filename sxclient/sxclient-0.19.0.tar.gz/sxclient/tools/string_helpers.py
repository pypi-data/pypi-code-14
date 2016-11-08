'''
Copyright (C) 2015-2016 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.
'''

from __future__ import unicode_literals

from typing import Union  # noqa

import six


__all__ = ['toutf8', 'tobytes']


def toutf8(text):
    # type: (Union[str, bytes]) -> str
    if isinstance(text, six.text_type):
        return text
    elif isinstance(text, six.binary_type):
        return text.decode('utf-8')
    else:
        raise TypeError(
            "Object is neither 'str' nor 'unicode': {}".format(repr(text))
        )


def tobytes(text):
    # type: (Union[str, bytes]) -> bytes
    if isinstance(text, six.text_type):
        return text.encode('utf-8')
    elif isinstance(text, six.binary_type):
        return text
    else:
        raise TypeError(
            "Object is neither 'str' nor 'unicode': {}".format(repr(text))
        )
