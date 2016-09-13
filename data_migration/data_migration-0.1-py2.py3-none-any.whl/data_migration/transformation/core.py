# -*- coding: utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
#
# This file is part of Canopsis.
#
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

from data_migration.patch.core import getpatch
from data_migration.patch.core import Patch
from data_migration.lang.json import JsonSchema

class Transformation(object):

    def __init__(self, schema):

        super(Transformation, self).__init__()

        self.schema = schema
        self.patch = getpatch(self.schema, self.schema['patch'])

    @property
    def input(self):

        return self.schema['input']

    @property
    def output(self):

        return self.schema['output']

    @property
    def filtre(self):

        return self.schema['filter']

    def select_data(self, filter, input):

        data = getresource(input)
        db.data.find(filter)

        return data

    def apply_patch(self, data=None):

        if data is None:

            data = self.select_data(self.filter, self.input)

        return self.patch.process(data, self.schema)

    def save(self, output):

        raise NotImplementedError()