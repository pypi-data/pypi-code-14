# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
# Canopsis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Canopsis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Canopsis.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------

_PATCHS = {}

def registerpatch(schemacls, cls=None):
    """decorator which get type (JSON, xslt, ...) of the patch
    and return it"""

    def _recordpatch(cls):

        _PATCHS[schemacls] = cls

        return cls

    if cls is None:
        return _recordpatch

    else:
        return _recordpatch(cls)


def getpatch(schema, patch):
    """return the correct patch, take 2 parameters
    schema, patch"""

    result = None

    cls = None

    for schemacls in _PATCHS:

        if isinstance(schema, schemacls):

            cls = _PATCHS[schemacls]
            break

    if cls is not None:
        result = cls(patch)

    if not result:
        raise(Exception('patch not found'))

    return result


class Patch(object):

    def __init__(self, patch):

        self.patch = patch

    def process(self, data, schema):

        raise NotImplementedError()
