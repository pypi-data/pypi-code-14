# vi:et:ts=4 sw=4 sts=4
#
# envconfig2: easily read your config from the environment
# Copyright (C) 2016  Gary Kramlich <grim@reaperworld.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

import json as realjson
import os


__version__ = '0.1'


def use_default(name, required):
    if name not in os.environ:
        if required:
            msg = 'required environmnet variable {} not set'.format(name)

            raise ValueError(msg)

        return True

    return False


def boolean(name, default=None, required=False):
    if use_default(name, required):
        return default

    val = os.environ[name].lower().strip()

    return val in ['1', 't', 'true', 'y', 'yes']


def integer(name, default=None, required=False):
    if use_default(name, required):
        return default

    return int(os.environ[name])


def string(name, default=None, required=False):
    if use_default(name, required):
        return default

    return os.environ[name]


def list(name, separator=',', default=None, required=False):
    if use_default(name, required):
        return default

    return [item.strip() for item in os.environ[name].split(separator)]


def json(name, default=None, required=False):
    if use_default(name, required):
        return default

    return realjson.loads(os.environ[name])

