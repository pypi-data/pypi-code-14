# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from envconf import Env

Django110Env = Env(
    DEBUG=(bool, False),
    SECRET_KEY=str,

)
