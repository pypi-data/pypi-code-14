# -*- coding: utf-8 -*-
#
# This file is part of Inspirehep.
# Copyright (C) 2016 CERN.
#
# Inspirehep is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Inspirehep is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Inspirehep; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

from __future__ import absolute_import, print_function

import json
from pyrsistent import freeze, thaw


class ConflictType(object):
    pass

_CONFLICTS = (
    'REORDER',
    'MANUAL_MERGE',
    'ADD_BACK_TO_HEAD',
    'SET_FIELD',
    'REMOVE_FIELD'
)
for conflict_type in _CONFLICTS:
    setattr(ConflictType, conflict_type, conflict_type)


class Conflict(tuple):
    """Immutable representation of a conflict."""

    # Based on http://stackoverflow.com/a/4828108
    # Compatible with Python<=2.6

    def __new__(cls, conflict_type, path, body):
        if conflict_type not in _CONFLICTS:
            raise ValueError('Bad Conflict Type %s' % conflict_type)
        body = freeze(body)
        return tuple.__new__(cls, (conflict_type, path, body))

    conflict_type = property(lambda self: self[0])
    path = property(lambda self: self[1])
    body = property(lambda self: thaw(self[2]))

    def with_prefix(self, root_path):
        return Conflict(self.conflict_type, root_path + self.path, self.body)

    def to_json(self):
        return json.dumps([self.conflict_type, self.path, self.body])
