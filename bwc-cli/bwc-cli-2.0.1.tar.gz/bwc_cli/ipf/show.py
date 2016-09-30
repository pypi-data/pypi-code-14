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


class ShowConfigBGP(command.Command):
    """Display Fabric configuration for the specified Fabric"""

    ref_or_id = 'bwc-topology.show_config_bgp'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowConfigBGP, self).get_parser(prog_name)
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
        result = result_json['result']
        print('Show BGP Configuration')
        self.log.info(result)


class ShowTopology(command.Command):
    """Generates Topology for the specified Fabric"""

    ref_or_id = 'bwc-topology.topology_generate'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowTopology, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            metavar='<fabric>',
            default='default',
            help='Fabric name for which topology will be displayed',
        )

        parser.add_argument(
            '--format',
            metavar='<format>',
            default='pdf',
            help='Format of the file to generate for the topology',
        )
        parser.add_argument(
            '--render_dir',
            metavar='<render_dir>',
            default='/tmp',
            help='Path where the topology file will be saved',
        )

        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        result = result_json['result']
        self.log.info('Show Topology')
        print(result)
