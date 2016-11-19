import pytest
from cifsdk_zyre import Zyre
from cifsdk.client.http import Client
from pyzyre.client import Client
from pyzyre.chat import task
from zmq.eventloop import ioloop
from time import sleep
from csirtg_indicator import Indicator
import zmq
import sys
import json

from pprint import pprint

@pytest.fixture
def iface():
    if sys.platform == 'darwin':
        return 'en0'
    else:
        return 'eth0'


def test_zyre(iface):
    ioloop.install()
    loop = ioloop.IOLoop.instance()
    loop2 = ioloop.IOLoop.instance()

    client = Client(
        group='TEST',
        loop=loop,
        verbose=1,
        interface=iface,
        task=task,
    )

    client.start_zyre()

    client2 = Zyre(
        group='TEST',
        loop=loop2,
        verbose=1,
        interface=iface,
        task=task,
    )

    client2.start()

    sleep(0.01)

    def test_fcn(*args):
        i = Indicator('example.com')
        client.send_message(str(i))

    def test_fcn2(s, e):
        m = s.recv_multipart()
        assert m[0] == 'ENTER'
        m = s.recv_multipart()
        assert m[0] == 'JOIN'
        m = s.recv_multipart()
        assert m[0] == 'SHOUT'

        i = json.loads(m[4])
        i = Indicator(**i)

        assert i.indicator == 'example.com'

    loop2.add_handler(client2.actor, test_fcn2, zmq.POLLIN)

    loop.add_handler(client.actor, test_fcn, zmq.POLLIN)
    loop.run_sync(test_fcn)

    client.stop_zyre()
    client2.stop()



