#!/usr/bin/env python

import logging
import os.path
import select
import textwrap
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from cifsdk.constants import REMOTE_ADDR, TOKEN
from cifsdk.utils import setup_logging, get_argument_parser
from csirtg_indicator import Indicator
from cifsdk.client.http import HTTP as HTTPClient
from pprint import pprint
from czmq import Zactor, zactor_fn, create_string_buffer
from time import sleep
from pyzyre.chat import task
import zmq
from zmq.eventloop import ioloop
import json

GROUP = os.environ.get('CIF_ZYRE_GROUP', 'ZYRE')
INTERFACE = os.environ.get('CIF_ZYRE_INTERFACE', 'tap0')
EVASIVE_TIMEOUT = os.environ.get('ZYRE_EVASIVE_TIMEOUT', 5000)  # zyre defaults
EXPIRED_TIMEOUT = os.environ.get('ZYRE_EXPIRED_TIMEOUT', 30000)

logger = logging.getLogger(__name__)


class Zyre(object):
    def __init__(self, group=GROUP, interface=INTERFACE, **kwargs):
        self.group = group
        self.interface = interface

        self.actor = None
        self._actor = None

        self.task = zactor_fn(task)

        actor_args = [
            'channel=%s' % self.group,
            'beacon=1',
        ]

        actor_args = ','.join(actor_args)
        self.actor_args = create_string_buffer(actor_args)

        logger.info('staring zyre...')

        # disable CZMQ from capturing SIGINT
        os.environ['ZSYS_SIGHANDLER'] = 'false'

        # signal zbeacon in czmq
        if not os.environ.get('ZSYS_INTERFACE'):
            os.environ["ZSYS_INTERFACE"] = self.interface

    def start(self):
        self._actor = Zactor(self.task, self.actor_args)
        self.actor = zmq.Socket(shadow=self._actor.resolve(self._actor).value)
        sleep(0.1)
        logger.info('zyre started')

    def stop(self):
        logger.info('stopping zyre')
        self.actor.send_multipart(['$$STOP', ''.encode('utf-8')])
        sleep(0.01)  # cleanup
        logger.info('stopping zyre')
        self.actor.close()
        del self._actor


def main():
    p = get_argument_parser()
    p = ArgumentParser(
        description=textwrap.dedent('''\
        Environmental Variables:
            CIF_ZYRE_INTERFACE
            CIF_ZYRE_REMOTE
            CIF_ZYRE_TOKEN
            CIF_ZYRE_PROVIDERS
            CIF_ZYRE_ITYPE
            CIF_ZYRE_TAGS
            CIF_ZYRE_CONFIDENCE

        example usage:
            $ cif-zyre --remote https://cif.example.com --token 1234
            $ cif-zyre -i tap0 -d --providers site1.example.com,site2.example.com
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cif-zyre',
        parents=[p]
    )

    p.add_argument('--token', help='specify api token', default=TOKEN)
    p.add_argument('--remote', help='specify API remote [default %(default)s]', default=REMOTE_ADDR)
    p.add_argument('-p', '--ping', action="store_true") # meg?
    p.add_argument('-q', '--search', help="search")
    p.add_argument('--itypes', help='filter by indicator type [csv]')
    p.add_argument('-i', '--interface')
    p.add_argument('-g', '--group')

    p.add_argument('--tags', nargs='+')
    p.add_argument('--provider')
    p.add_argument('--confidence', help="specify confidence level")

    p.add_argument('--no-verify-ssl', action='store_true')

    args = p.parse_args()

    setup_logging(args)
    logger = logging.getLogger(__name__)

    verify_ssl = True
    if args.no_verify_ssl:
        verify_ssl = False

    if args.remote == 'https://localhost':
        verify_ssl = False

    cli = HTTPClient(args.remote, args.token, verify_ssl=verify_ssl)

    def handle_message(s, e):
        m = s.recv_multipart()

        logger.debug(m)

        m_type = m.pop(0)

        logger.info(m_type)

        if m_type == 'ENTER':
            logger.info("ENTER {}".format(m))

        elif m_type == 'SHOUT':
            group, peer, address, message = m
            logger.info('[SHOUT:{}] {}'.format(peer, message))
            m = json.loads(message)
            i = Indicator(**m)
            rv = cli.indicators_create(i)

            logger.info('success id: {}'.format(rv))

        else:
            logger.warn("unhandled m_type {} rest of message is {}".format(m_type, m))

    ioloop.install()
    loop = ioloop.IOLoop.instance()

    client = Zyre(
        group=args.group,
        loop=loop,
        verbose=args.debug,
        interface=args.interface,
        task=task
    )

    client.start()

    loop.add_handler(client.actor, handle_message, zmq.POLLIN)

    try:
        loop.start()
    except KeyboardInterrupt:
        logger.info('SIGINT Received')
    except Exception as e:
        logger.error(e)

    client.stop()


if __name__ == "__main__":
    main()