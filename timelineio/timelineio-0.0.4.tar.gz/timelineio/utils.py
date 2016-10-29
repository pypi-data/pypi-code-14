# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import distutils
import os


def env_to_bool(env_name, default=False):
    env = os.environ.get(env_name)
    if env is None:
        return default
    return bool(distutils.util.strtobool(env))
