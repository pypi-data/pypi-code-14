# -*- coding: utf-8 -*-
# Copyright (c) 2016 Sqreen. All Rights Reserved.
# Please refer to our terms for more information: https://www.sqreen.io/terms.html
""" Environment helpers
"""

import os


def get(name, default=None):
    """ Alias for os.getenv
    """
    return os.getenv(name, default=default)


def get_env_or_fail(name):
    """ Try to get environment variable via os.getenv.
    If it's not defined, raise a ValueError
    """
    res = os.getenv(name)
    if res is None:
        raise ValueError("environment variable %r is not defined" % name)
    else:
        return res
