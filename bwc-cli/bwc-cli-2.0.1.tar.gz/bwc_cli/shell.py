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
import logging.config
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from st2client.utils.logging import LogLevelFilter
from st2client.config import set_config
from st2client.base import BaseCLIApp

from bwc_cli import __version__

__all__ = [
    'BWCCLIApp'
]

LOGGER = logging.getLogger(__name__)

CLI_DESCRIPTION = 'Brocade Workflow composer CLI'


class BWCCLIApp(BaseCLIApp, App):
    LOG = LOGGER

    def __init__(self):
        super(BWCCLIApp, self).__init__(
            description=CLI_DESCRIPTION,
            version=__version__,
            command_manager=CommandManager('bwc.ipf'),
            deferred_help=True,
        )

        # Set up of endpoints is delayed until program is run.
        self.client = None

    def build_option_parser(self, description, version):
        parser = super(BWCCLIApp, self).build_option_parser(
            description,
            version
        )

        # Global arguments/ options
        parser.add_argument(
            '--config-file',
            action='store',
            dest='config_file',
            default=None,
            help='Path to the CLI config file'
        )

        parser.add_argument(
            '--print-config',
            action='store_true',
            dest='print_config',
            default=False,
            help='Parse the config file and print the values'
        )

        parser.add_argument(
            '--skip-config',
            action='store_true',
            dest='skip_config',
            default=False,
            help='Don\'t parse and use the CLI config file'
        )

        return parser

    def initialize_app(self, argv):
        result = super(BWCCLIApp, self).initialize_app(argv)

        args = self.options
        config = self._parse_config_file(args=args)
        set_config(config=config)

        self.client = self.get_client(args=args, debug=args.debug)
        return result

    def run(self, argv):
        return super(BWCCLIApp, self).run(argv)


def setup_logging(argv):
    debug = '--debug' in argv

    root = LOGGER
    root.setLevel(logging.WARNING)

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s  %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if not debug:
        handler.addFilter(LogLevelFilter(log_levels=[logging.ERROR]))

    root.addHandler(handler)

    if debug:
        logging.getLogger('requests').setLevel(logging.DEBUG)
    else:
        logging.getLogger('requests').setLevel(logging.WARNING)


def main(argv=sys.argv[1:]):
    setup_logging(argv)
    return BWCCLIApp().run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
