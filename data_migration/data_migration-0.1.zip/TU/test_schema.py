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

"""
test the correct running of Schema API
"""

from data_migration.core import Schema
from data_migration.lang.json import JsonSchema
from data_migration.transformation.core import Transformation

from unittest import main, TestCase, SkipTest
import jsonpatch
import jsonschema
import json

class TestSchema(TestCase):

    schema_class = None

    path = None

    def setUp(self):
        """parameters definition function"""

        if self.schema_class is None:
            raise SkipTest('Schema class is not given in {0}'.format(self))

        self.schema = self.schema_class(self.path)


class TestLoadSchema(TestSchema):
    """schema are in a specific folder, we load it raise an error if schema does not exist"""

    path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/transformation_schema.json'

    def setUp(self):
        """parameters definition function"""

        super(TestLoadSchema, self).setUp()

        self.paths = '/home/julie/Documents/canopsis/sources/python/schema/etc/schemma'

    def test_success(self):
        """API take a path, return a schema"""

        schema = self.schema.getresource(self.path)


    def test_failed(self):
        """Api take a non existing path raise an error"""

        with self.assertRaises(IOError):
            schema = self.schema.getresource(self.paths)


class TestSchemaDict(TestSchema):
    """test if returned schema can be used like a dictionary
        get an item from the loaded schema
        set a value in the item
        del item
        raise an error if schema is not a dict"""

    path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/transformation_schema.json'

    def test_get(self):
        """test to get an element from schema"""

        element = self.schema['id']
        self.assertEqual(element, "http://canopsis.org/transformation_schema.json")

    def test_set(self):
        """test to set a value in the schema"""
        self.schema['name'] = 'essai'
        self.assertEqual('essai', self.schema['name'])

    def test_del(self):
        """test to delete an element from the schema"""
        del self.schema['name']
        with self.assertRaises(KeyError):
            self.schema['name']

class TestValidateSchema(TestSchema):
    """test schema validation"""

    path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/V1_schema.json'

    def setUp(self):

        super(TestValidateSchema, self).setUp()

        self.doc = {"version":"1.0.0"}

    def test_validation(self):
        """validate a schema return none"""

        self.assertIsNone(self.schema.validate(self.doc))

class TestTransformation(TestSchema):
    """to transform data we need to get informations from transformation schema
    raise errors if information doesn't exist"""

    path = '/home/julie/Documents/canopsis/sources/python/schema/etc/schema/patch.json'

    def setUp(self):

        super(TestTransformation, self).setUp()
        self.transfo = self.transformation_class(self.schema)

    def test_select_data(self):
        """test application of the filter for data selection"""

        schema = self.schema.getresource(self.path)
        self.schema.validate(schema)

    def test_apply_patch(self):
        """take the selected data and apply patch process
        return the transform data"""

        schema = self.schema.getresource(self.path)
        data =  {   "version":"1.0.0",
                    "info":{
                        "eids":"bla"
                    }
                }

        result = self.transfo.apply_patch(data)
        self.assertEqual(result, {'info': {u'entity_id': 'bla'}, u'essai1': 'test1', 'version': '2.0.0'})


if __name__ == '__main__':
    main()