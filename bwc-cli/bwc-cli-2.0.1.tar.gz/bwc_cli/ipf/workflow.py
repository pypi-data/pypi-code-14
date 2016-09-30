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


class WorkflowBGP(command.Command):
    """Execute the IP Fabric Workflow and display the details"""

    ref_or_id = 'bwc-ipfabric.configure_fabric'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(WorkflowBGP, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            metavar='<fabric>',
            help='Fabric on which the BGP workflow will be executed',
        )
        return parser

    def take_action(self, parsed_args):
        # The response of this is tricky. The last step in the Workflow is what
        # we will display.
        # Success or Failure will be done for the last set of the workflow.
        self.log.info('IP Fabric Workflow')
        print('Workflow: %s' % (parsed_args.ref_or_id))
        print('Status: %s' % (parsed_args.execution_status))
        print('Id: %s' % (parsed_args.execution_id))
        result_json = parsed_args.result
        tasks = result_json['tasks']
        final_task = tasks[-1]
        print(final_task['result']['result'])
