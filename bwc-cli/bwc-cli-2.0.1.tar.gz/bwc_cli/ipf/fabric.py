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


class FabricAdd(command.Command):
    """Add a new Fabric"""
    ref_or_id = 'bwc-topology.fabric_add'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FabricAdd, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            help='Name of the fabric to be added',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        data = result_json['result']['Fabric']
        self.log.info('Fabric %s Added successfully' % data)


class FabricDelete(command.Command):
    """Delete an existing Fabric"""

    ref_or_id = 'bwc-topology.fabric_delete'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FabricDelete, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            metavar='<fabric>',
            help='Name of the fabric to be deleted',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        data = result_json['result']['Fabric']
        self.log.info('Fabric %s deleted successfully' % data)


class FabricList(command.Command):
    """List all the Fabrics"""

    ref_or_id = 'bwc-topology.fabric_list'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FabricList, self).get_parser(prog_name)
        parser.add_argument(
            '--fabric',
            metavar='<fabric>',
            help='Fabric for which the configuration will be displayed',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        self.log.info('Fabric Listing')
        op_string = ''
        if parsed_args.fabric is not None:
            op_string += 'Fabric Name: ' + result_json['result']['fabric_name'] + '\n'
            for key, value in result_json['result']['fabric_settings'].items():
                op_string += key + ' : ' + value + '\n'
        else:
            for data in result_json['result']:
                op_string += 'Fabric Name: ' + data['fabric_name'] + '\n'
                for key, value in data['fabric_settings'].items():
                    op_string += key + ' : ' + value + '\n'
                op_string += '\n'
        print(op_string)


class FabricConfigShow(command.ShowOne):
    """Display Fabric configuration for the specified Fabric"""

    ref_or_id = 'bwc-topology.fabric_list'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FabricConfigShow, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            help='Fabric for which the configuration will be displayed',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        self.log.info('Fabric Config Show')
        columnnames = ['Fabric Name']
        data = [result_json['result']['fabric_name']]
        for key, value in result_json['result']['fabric_settings'].items():
            columnnames.append(key)
            data.append(value)
        return (tuple(columnnames), tuple(data))


class FabricConfigSet(command.Command):
    """Set or update Fabric properties"""

    ref_or_id = 'bwc-topology.fabric_config_set'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FabricConfigSet, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            help='Fabric for which the key value pair will be set',
        )
        parser.add_argument(
            'key',
            metavar='<key>',
            help='Key to be assigned to the fabric',
        )
        parser.add_argument(
            'value',
            metavar='<value>',
            help='Value to be specified for the key',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        for key, value in result_json['result'].items():
            print('Setting %s with value %s added to fabric %s' % (key, value, parsed_args.fabric))


class FabricConfigDelete(command.Command):
    """Delete Fabric property"""

    ref_or_id = 'bwc-topology.fabric_config_delete'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(FabricConfigDelete, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            metavar='<fabric>',
            help='Fabric for which the key value pair will be deleted',
        )
        parser.add_argument(
            'key',
            metavar='<key>',
            help='Key to be deleted from the fabric',
        )

        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        data = result_json['result']['Key']
        fabric = result_json['result']['Fabric']
        self.log.info('Key %s deleted successfully from fabric %s ' % (data, fabric))
