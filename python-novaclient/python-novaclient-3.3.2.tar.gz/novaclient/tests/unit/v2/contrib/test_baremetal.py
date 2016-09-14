# Copyright 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from novaclient import extension
from novaclient.tests.unit import utils
from novaclient.tests.unit.v2.contrib import fakes
from novaclient.v2.contrib import baremetal


extensions = [
    extension.Extension(baremetal.__name__.split(".")[-1], baremetal),
]
cs = fakes.FakeClient(extensions=extensions)


class BaremetalExtensionTest(utils.TestCase):

    def test_list_nodes(self):
        nl = cs.baremetal.list()
        self.assert_request_id(nl, fakes.FAKE_REQUEST_ID_LIST)
        cs.assert_called('GET', '/os-baremetal-nodes')
        for n in nl:
            self.assertIsInstance(n, baremetal.BareMetalNode)

    def test_get_node(self):
        n = cs.baremetal.get(1)
        self.assert_request_id(n, fakes.FAKE_REQUEST_ID_LIST)
        cs.assert_called('GET', '/os-baremetal-nodes/1')
        self.assertIsInstance(n, baremetal.BareMetalNode)

    def test_create_node(self):
        n = cs.baremetal.create("service_host", 1, 1024, 2048,
                                "aa:bb:cc:dd:ee:ff")
        self.assert_request_id(n, fakes.FAKE_REQUEST_ID_LIST)
        cs.assert_called('POST', '/os-baremetal-nodes')
        self.assertIsInstance(n, baremetal.BareMetalNode)

    def test_delete_node(self):
        n = cs.baremetal.get(1)
        ret = cs.baremetal.delete(n)
        self.assert_request_id(ret, fakes.FAKE_REQUEST_ID_LIST)
        cs.assert_called('DELETE', '/os-baremetal-nodes/1')

    def test_node_add_interface(self):
        i = cs.baremetal.add_interface(1, "bb:cc:dd:ee:ff:aa", 1, 2)
        self.assert_request_id(i, fakes.FAKE_REQUEST_ID_LIST)
        cs.assert_called('POST', '/os-baremetal-nodes/1/action')
        self.assertIsInstance(i, baremetal.BareMetalNodeInterface)

    def test_node_remove_interface(self):
        ret = cs.baremetal.remove_interface(1, "bb:cc:dd:ee:ff:aa")
        self.assert_request_id(ret, fakes.FAKE_REQUEST_ID_LIST)
        cs.assert_called('POST', '/os-baremetal-nodes/1/action')

    def test_node_list_interfaces(self):
        il = cs.baremetal.list_interfaces(1)
        self.assert_request_id(il, fakes.FAKE_REQUEST_ID_LIST)
        cs.assert_called('GET', '/os-baremetal-nodes/1')
