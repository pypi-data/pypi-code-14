# Licensed to the Brocade, Inc. ('Brocade') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from bwc_cli.common import command


class InventoryAdd(command.Lister):
    """Add devices to a Fabric"""

    ref_or_id = 'bwc-topology.switch_add'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InventoryAdd, self).get_parser(prog_name)
        parser.add_argument(
            'host',
            help='IP of the device to be deleted',
        )
        parser.add_argument(
            'fabric',
            help='Fabric to which the device will be added',
        )
        parser.add_argument(
            'user',
            help='Username to connect to the device',
        )
        parser.add_argument(
            'passwd',
            help='Password to connect to the device',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        res = []
        if type(result_json['result']) == list:
            res = result_json['result']
        else:
            res.append(result_json['result'])
        columns = ('IP', 'Model', 'Rbridge-Id', 'Firmware', 'Name', 'Role', 'ASN', 'Fabric')
        self.log.info('Inventory Add')
        return (columns,
                ((n['ip_address'], n['model'], n['rbridge_id'], n['firmware'], n['name'],
                  n['role'], n['asn'], n['fabric']['fabric_name']) for n
                 in res)
                )


class InventoryDelete(command.Lister):
    """Delete device"""

    ref_or_id = 'bwc-topology.switch_delete'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InventoryDelete, self).get_parser(prog_name)
        parser.add_argument(
            'host',
            help='IP of the device to be deleted',
        )

        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        res = []
        if type(result_json['result']) == list:
            res = result_json['result']
        else:
            res.append(result_json['result'])
        columns = ('IP', 'Model', 'Rbridge-Id', 'Firmware', 'Name', 'Role', 'ASN', 'Fabric')
        self.log.info('Inventory delete')
        return (columns,
                ((n['ip_address'], n['model'], n['rbridge_id'], n['firmware'], n['name'],
                  n['role'], n['asn'], n['fabric']['fabric_name']) for n
                 in res)
                )


class InventoryUpdate(command.Lister):
    """Update inventory details for the specified device or entire Fabric"""

    ref_or_id = 'bwc-topology.switch_update'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InventoryUpdate, self).get_parser(prog_name)
        list_group = parser.add_mutually_exclusive_group(required=True)
        list_group.add_argument(
            '--host',
            default=None,
            help='IP of the device to be updated',
        )
        list_group.add_argument(
            '--fabric',
            default=None,
            help='Name of the fabric to update all devices',
        )
        parser.add_argument(
            '--user',
            help='Username to connect to the device(s)',
        )
        parser.add_argument(
            '--passwd',
            help='Password to connect to the device(s)',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        res = []
        if not result_json['result'] or len(result_json['result']) == 0:
            self.log.info('No device(s) updated')
            return ''
        else:
            for i in result_json['result']:
                res.append(i[1])
            columns = ('IP', 'Model', 'Rbridge-Id', 'Firmware', 'Name', 'Role', 'ASN', 'Fabric')
            self.log.info('Inventory Update')
            return (columns,
                    ((n['ip_address'], n['model'], n['rbridge_id'], n['firmware'],
                      n['name'],
                      n['role'], n['asn'], n['fabric']['fabric_name']) for n
                     in res)
                    )


class InventoryList(command.Lister):
    """List a specific device details or all the devices in the specified Fabric"""

    ref_or_id = 'bwc-topology.switch_list'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InventoryList, self).get_parser(prog_name)
        list_group = parser.add_mutually_exclusive_group(required=True)
        list_group.add_argument(
            '--host',
            default=None,
            help='IP of the device to be listed',
        )
        list_group.add_argument(
            '--fabric',
            default=None,
            help='Name of the fabric to list all devices',
        )
        return parser

    def take_action(self, parsed_args):

        result_json = parsed_args.result
        res = []
        if type(result_json['result']) == list:
            res = result_json['result']
        else:
            res.append(result_json['result'])

        columns = ('IP', 'Model', 'Rbridge-Id', 'Firmware', 'Name', 'Role', 'ASN', 'Fabric')
        self.log.info('Inventory List')
        return (columns,
                ((n['ip_address'], n['model'], n['rbridge_id'], n['firmware'], n['name'],
                  n['role'], n['asn'], n['fabric']['fabric_name']) for n
                 in res)
                )


class InventoryShowLLDP(command.Lister):
    """List LLDP details for the specified switch or fabric"""

    ref_or_id = 'bwc-topology.show_lldp_links'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InventoryShowLLDP, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            default='Default',
            help='Name of the fabric to list all devices',
        )
        return parser

    def take_action(self, parsed_args):

        result_json = parsed_args.result
        self.log.info('Inventory Show LLDP')
        columns = ('IP', 'Local MAC', 'Local Intf', 'Remote MAC', 'Remote Intf',
                   'Remote System', 'Remote Management Addr')
        return (columns,
                ((n['ip_address'], lldp_data['local_int_mac'], lldp_data['local_int_name'],
                  lldp_data['remote_int_mac'], lldp_data['remote_int_name'], lldp_data[
                      'remote_management_address'], lldp_data['remote_system_name']) for
                 n in
                    result_json['result'] for lldp_data in n['lldp_data']))


class InventoryShowVcs(command.Lister):
    """List VCS link details for the specified switch or fabric"""

    ref_or_id = 'bwc-topology.show_vcs_links'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(InventoryShowVcs, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            help='Name of the fabric to list all devices',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        self.log.info('Inventory Show VCS')
        columns = ('Interface-1', 'IP-1', 'Interface-2', 'IP-2', 'Fabric')
        return (columns,
                ((n[0]['interface'], n[0]['ip_address'], n[1]['interface'], n[1]['ip_address'],
                  n[0]['fabric']) for n
                 in result_json[
                     'result'])
                )
