# -*- coding:utf-8 -*-
from __future__ import unicode_literals, absolute_import

from flask import __version__ as flask_version


def is_flask_legacy():
    v = flask_version.split(".")
    return int(v[0]) == 0 and int(v[1]) < 11
