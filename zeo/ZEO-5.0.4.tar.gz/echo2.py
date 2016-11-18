"""Demonstrate problem with asyncio server handling connections that disconnect immediately

Run with 3.4 and 4.5, this script hangs.

(There are actually at least 2 problems.  In addition to the hang,
there's a problem in _selector_events._SelectorTransport._fatal_error,
where it tries to use self._loop, which is None.)
"""

import asyncio
import socket
import struct
import sys
import threading
import time
from queue import Queue

class EchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.transport = transport
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        sys.stdout.flush()
        transport.write(b'SERVER')

    def data_received(self, data):
        print('server received:', data)
        sys.stdout.flush()
        self.transport.write(b'RESPOND ' + data)

    def connection_lost(self, exc):
        print('The client closed the connection')
        sys.stdout.flush()

def run_server(queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    coro = loop.create_server(EchoServerProtocol, '127.0.0.1', 8888)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    sys.stdout.flush()
    queue.put(1)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

class EchoClientProtocol(asyncio.Protocol):

    def __init__(self, loop):
        self.loop = loop

        self.messages = [b'MESSAGE', b'CLIENT']

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('Client received:', data)
        sys.stdout.flush()
        if self.messages:
            message = self.messages.pop()
            self.transport.write(message)
            print('Client sent:', message)
        else:
            print('Client closing')
            self.transport.close()

    def connection_lost(self, exc):
        print('The server closed the connection')
        sys.stdout.flush()
        self.loop.stop()

queue = Queue()
thread = threading.Thread(target=run_server, args=(queue,), daemon=True)
thread.start()
queue.get()

time.sleep(1)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

for i in range(20):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                 struct.pack('ii', 1, 0))
    s.connect(('127.0.0.1', 8888))
    s.close()

coro = loop.create_connection(lambda: EchoClientProtocol(loop),
                              '127.0.0.1', 8888)
asyncio.async(coro, loop=loop)
loop.run_forever()

print('Done')

loop.close()
