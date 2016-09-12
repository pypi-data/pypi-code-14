# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import ddt
import mock
import socket
import uuid

from oslo_config import cfg

from kuryr.lib import constants as const
from kuryr.lib import utils
from kuryr.tests.unit import base


@ddt.ddt
class TestKuryrUtils(base.TestCase):
    """Unit tests for utilities."""
    def setUp(self):
        super(TestKuryrUtils, self).setUp()
        self.fake_url = 'http://127.0.0.1:9696'
        self.fake_auth_url = 'http://127.0.0.1:35357/v2.0'

    def test_get_veth_pair_names(self):
        fake_neutron_port_id = str(uuid.uuid4())
        generated_ifname, generated_peer = utils.get_veth_pair_names(
            fake_neutron_port_id)

        namelen = const.NIC_NAME_LEN
        ifname_postlen = namelen - len(const.VETH_PREFIX)
        peer_postlen = namelen - len(const.CONTAINER_VETH_PREFIX)

        self.assertEqual(namelen, len(generated_ifname))
        self.assertEqual(namelen, len(generated_peer))
        self.assertIn(const.VETH_PREFIX, generated_ifname)
        self.assertIn(const.CONTAINER_VETH_PREFIX, generated_peer)
        self.assertIn(fake_neutron_port_id[:ifname_postlen], generated_ifname)
        self.assertIn(fake_neutron_port_id[:peer_postlen], generated_peer)

    def test_get_subnetpool_name(self):
        fake_subnet_cidr = "10.0.0.0/16"
        generated_neutron_subnetpool_name = utils.get_neutron_subnetpool_name(
            fake_subnet_cidr)
        name_prefix = cfg.CONF.subnetpool_name_prefix
        self.assertIn(name_prefix, generated_neutron_subnetpool_name)
        self.assertIn(fake_subnet_cidr, generated_neutron_subnetpool_name)

    @mock.patch('neutronclient.v2_0.client.Client')
    @mock.patch('keystoneauth1.loading.load_auth_from_conf_options')
    @mock.patch('keystoneauth1.loading.load_session_from_conf_options')
    def test_get_neutron_client(self, mock_session_loader, mock_auth_loader,
                                mock_client):
        fake_auth = 'Fake_auth_plugin'
        fake_session = 'Fake_session_plugin'
        mock_auth_loader.return_value = fake_auth
        mock_session_loader.return_value = fake_session
        utils.get_neutron_client()
        mock_client.assert_called_once_with(
            auth=fake_auth,
            session=fake_session,
            endpoint_type=cfg.CONF.neutron.endpoint_type)

    @mock.patch.object(socket, 'gethostname', return_value='fake_hostname')
    def test_get_hostname(self, mock_get_hostname):
        self.assertEqual('fake_hostname', utils.get_hostname())
        mock_get_hostname.assert_called_once()

    def test_get_dict_format_fixed_ips_from_kv_format(self):
        fake_fixed_ips_kv_format = \
            ['subnet_id=5083bda8-1b7c-4625-97f3-1d4c33bfeea8',
             'ip_address=192.168.1.2',
             'subnet_id=6607a230-f3eb-4937-b09f-9dd659211139',
             'ip_address=fdfa:8456:1afa:0:f816:3eff:fe67:885e']
        expected_dict_form = \
            [{'subnet_id': '5083bda8-1b7c-4625-97f3-1d4c33bfeea8',
              'ip_address': '192.168.1.2'},
             {'subnet_id': '6607a230-f3eb-4937-b09f-9dd659211139',
              'ip_address': 'fdfa:8456:1afa:0:f816:3eff:fe67:885e'}]
        fixed_ips = utils.get_dict_format_fixed_ips_from_kv_format(
                        fake_fixed_ips_kv_format)
        self.assertEqual(expected_dict_form, fixed_ips)

    def test_string_mappings(self):
        fake_mapping_list = {'fake_key': 'fake_value'}
        fake_result = '"{\'fake_key\': \'fake_value\'}"'
        self.assertEqual(fake_result, utils.string_mappings(fake_mapping_list))

    def test_get_random_string(self):
        fake_string_len = 20
        self.assertEqual(fake_string_len,
             len(utils.get_random_string(fake_string_len)))
