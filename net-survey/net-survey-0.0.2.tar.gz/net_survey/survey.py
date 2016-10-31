"""
   Copyright 2016 Net-Survey

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from client.client import NSClient
from server.api import APIServer
from interfaces import NetworkInterfaces
import logging
import multiprocessing
from oslo_config import cfg
from oslo_config import types
import pkg_resources
import signal
import sys
from server.server import NSServer

PortType = types.Integer(1, 65535)

_cli_opts = [
    cfg.StrOpt('mode',
               default='client',
               help='Survey mode: server or client.'),
    cfg.StrOpt('bind_host',
               default='0.0.0.0',
               help='IP Address to listen on.'),
    cfg.Opt('bind_port',
            type=PortType,
            default=4000,
            help='Port to listen on.'),
    cfg.StrOpt('server_ip',
               default='127.0.0.1',
               help='IP Address of survey master server.'),
    cfg.Opt('server_port',
            type=PortType,
            default=4000,
            help='Port to connect to the server on.'),
    cfg.Opt('server_api_port',
            type=PortType,
            default=8000,
            help='HTTP API Port.'),
    cfg.StrOpt('inventory_file',
               default='/etc/net-survey/inventory.ini',
               help='Inventory file used for client connections.'),
    cfg.BoolOpt('use_log_file',
                default=True,
                help='Use log file for output True/False or yes/no.'),
    cfg.StrOpt('log_file',
               default='/var/log/net-survey/survey.log',
               help='Log file location.'),
    cfg.StrOpt('log_level',
               default='INFO',
               help='Logging level: DEBUG, INFO, WARNING, ERROR, etc.'),
]


def register_cli_opts(conf):
    """Register net-survey cli options.

    :param conf: a ConfigOpts instance
    :raises: DuplicateOptError, ArgsAlreadyParsedError
    """
    conf.register_cli_opts(_cli_opts)


def _setup_logging(conf):
    """Setup logging level and output file.

    :param conf: a ConfigOpts instance
    :raises: KeyError
    """
    _levels = {
        'CRITICAL': 50,
        'ERROR': 40,
        'WARNING': 30,
        'INFO': 20,
        'DEBUG': 10,
        'NOTSET': 0
    }

    try:
        _conf_level = _levels[conf.log_level.upper()]
        if bool(conf.use_log_file):
            logging.basicConfig(filename=conf.log_file, level=_conf_level)
        else:
            logging.basicConfig(level=_conf_level)
    except Exception as e:
        logging.basicConfig(level=_levels['DEBUG'])
        logging.error('Error setting log level: %s' % str(e))


def main(args=None):
    """The main function of net-survey."""
    version = pkg_resources.get_distribution('oslo.config').version
    conf = cfg.ConfigOpts()
    register_cli_opts(conf)
    conf(args, version=version)
    _setup_logging(conf)

    if conf.mode == 'server':
        if not conf.inventory_file:
            logging.critical('Inventory file must be speicified when running'
                             ' in server mode.')
            sys.exit(1)
        # Setup dashboard event and queue
        _queue = multiprocessing.Queue()
        _api_event = multiprocessing.Event()
        _scan_event = multiprocessing.Event()

        # Start Net-Survey Server
        srv = NSServer(_queue, _api_event, _scan_event, conf)
        signal.signal(signal.SIGTERM, srv.terminate)
        signal.signal(signal.SIGINT, srv.terminate)
        srv.start()

        # Start API server
        api_srv = APIServer(_queue, _api_event, _scan_event, conf)
        signal.signal(signal.SIGTERM, api_srv.terminate)
        signal.signal(signal.SIGINT, api_srv.terminate)
        api_srv.start()
    else:
        cli = NSClient(conf, NetworkInterfaces())
        signal.signal(signal.SIGTERM, cli.terminate)
        signal.signal(signal.SIGINT, cli.terminate)
        cli.start()


if __name__ == '__main__':
    main()
