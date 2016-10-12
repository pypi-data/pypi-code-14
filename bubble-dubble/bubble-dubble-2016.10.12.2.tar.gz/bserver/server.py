#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import asyncio
import simplejson as json
from concurrent import futures
from bubble.bcommon import default
from bubble.bserver.worker import BubbleWorker


class BubbleProtocol(asyncio.Protocol):
    worker = BubbleWorker()

    def connection_made(self, transport):
        self.transport = transport
        self.buffer = b''
        peername = transport.get_extra_info('peername')
        print('Connection from {}:{:d}'.format(*peername))
        self.worker.resetSent()

    def data_received(self, data):
        self.buffer += data
        buf = self.buffer.split(b'\r\n')
        self.buffer = buf[-1] if buf[-1] else b''
        for request in buf[:-1]:
            decoded_request = json.loads(request)
            response = self.worker.parse(decoded_request)
            response = '{}\r\n'.format(json.dumps(response))
            self.transport.write(response.encode())


def main():
    port = default.DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    loop = asyncio.get_event_loop()
    pool = futures.ThreadPoolExecutor(5)
    loop.set_default_executor(pool)
    coro = loop.create_server(BubbleProtocol, '0.0.0.0', port)
    server = loop.run_until_complete(coro)
    print('Bubble server integrator, (c) Vadim Dyadkin, ESRF, inspired by Giuseppe Portale')
    print('If you use this program, please cite this paper: http://dx.doi.org/10.1107/S1600577516002411')
    print('Mercurial repository: http://hg.3lp.cx/bubble')
    print('Mercurial hash: {}'.format(default.get_hg_hash()))
    print('Serving on {}:{:d}'.format(*server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('Ctrl-C has been pressed. Exit and clean up...')
    pool.shutdown()
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
