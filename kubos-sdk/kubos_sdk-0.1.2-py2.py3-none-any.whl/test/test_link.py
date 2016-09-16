# Kubos SDK
# Copyright (C) 2016 Kubos Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import kubos
import mock
import os
import unittest
import sys

from kubos.test.utils import get_arg_dict, KubosTestCase, remove_link
from kubos.utils.project import get_local_link_file, get_global_link_file, module_key, target_key


class KubosLinkTest(KubosTestCase):

    def setUp(self):
        super(KubosLinkTest, self).setUp()
        self.test_command = 'link'
        sys.argv.append(self.test_command)
        #These tests intentionally cause warnings output to stderr
        #These warnings aren't relevant to the test so this hides the warnings
        sys.stderr = open(os.devnull, 'wb')
        self.module_json = os.path.join(self.base_dir, 'module.json')


    def test_link_no_module_json(self):
        search_dict = {'subcommand_name' : self.test_command}
        with self.assertRaises(SystemExit):
            kubos.main()
            #There's no module.json in this folder


    def test_link_global(self):
        with open('module.json', 'w') as module_file:
            module_file.write(self.json_template)
        kubos.main()
        with open(get_global_link_file(), 'r') as link_file:
            link_data = json.load(link_file)
        self.assertTrue(self.test_name in link_data[module_key])


    def test_link_global_to_local(self):
        sys.argv.append(self.test_name) #Add the test_name value as the "module to link"
        kubos.main()
        with open(get_local_link_file(), 'r') as link_file:
            link_data = json.load(link_file)
        self.assertTrue(self.test_name in link_data[module_key])


    def test_link_relative_path(self):
        with open('module.json', 'w') as target_file:
            target_file.write(self.json_template)
        sys.argv.append(os.getcwd())
        kubos.main()
        with open(get_global_link_file(), 'r') as link_file:
            global_link_data = json.load(link_file)
        with open(get_local_link_file(), 'r') as link_file:
            local_link_data = json.load(link_file)
        self.assertTrue(self.test_name in global_link_data[module_key])
        self.assertTrue(self.test_name in local_link_data[module_key])


    def tearDown(self):
        super(KubosLinkTest, self).tearDown()
        if os.path.isfile(self.module_json):
            os.remove(self.module_json)


if __name__ == '__main__':
    unittest.main()
