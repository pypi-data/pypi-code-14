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

from data_migration.patch.core import Patch, registerpatch
from data_migration.lang.json import JsonSchema

import jsonpatch
import json


@registerpatch(JsonSchema)
class JSONPatch(Patch):

    def process(self, data, schema):
        """define the correct process to return the patch
        in the correct form and apply it on data"""

        patch = schema['patch']
        pa = []

        for element in patch:
            pa.append(patch[element])

        p = jsonpatch.JsonPatch(pa)
        result = p.apply(data)

        return result

    def save(self, new_data, output):

        with open('output', "w") as f:
            jdon.dump(new_data, output, sort_keys = True, indent = 2, separators = (',', ':'))
