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

from data_migration.core import Schema
from data_migration.lang.json import JsonSchema
from data_migration.transformation.core import Transformation
from data_migration.migration.factory import GLOBALFACTORY


def migrate(path_transfo):
    """the migrate function transform data and save them"""

    schema_class = JsonSchema
    transformation_class = Transformation

    schema = schema_class(path_transfo)
    transfo = transformation_class(schema)

    schema_transfo = schema.getresource(path_transfo)

    inp = schema_transfo['input']
    output = schema_transfo['output']
    path_v1 = schema_transfo['path_v1']
    path_v2 = schema_transfo['path_v2']

    schema_V1 = schema.getresource(path_v1)
    schema_V2 = schema.getresource(path_v2)

    myinp = GLOBALFACTORY.get(inp)
    data = myinp.load(inp, schema)
    result = myinp.transformation(inp, data, transfo, schema)

    myout = GLOBALFACTORY.get(output)
    myout.save(result, output, schema)