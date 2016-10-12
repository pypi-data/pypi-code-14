#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
import simplejson as json
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
