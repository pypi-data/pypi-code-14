"""Demonstrate problem with asyncio server handling connections that disconnect immediately

Run with 3.4 and 4.5, this script hangs.

(There are actually at least 2 problems.  In addition to the hang,
there's a problem in _selector_events._SelectorTransport._fatal_error,
where it tries to use self._loop, which is None.)
"""

import asyncio
import ssl
import sys
import threading
import time
from queue import Queue
from struct import unpack

class Base(asyncio.Protocol):

    def __init__(self):
        self.input  = [] # Input buffer when assembling messages
        self.output = [] # Output buffer when paused
        self.paused = [] # Paused indicator, mutable to avoid attr lookup


    closed = False
    def close(self):
        if not self.closed:
            self.closed = True
            if self.transport is not None:
                self.transport.close()

    def connection_made(self, transport):
        self.transport = transport
        paused = self.paused
        output = self.output
        append = output.append
        writelines = transport.writelines
        from struct import pack

        def write(message):
            if paused:
                append(message)
            else:
                writelines((pack(">I", len(message)), message))

        self._write = write

    got = 0
    want = 4
    getting_size = True
    def data_received(self, data):
        self.got += len(data)
        self.input.append(data)
        while self.got >= self.want:
            try:
                extra = self.got - self.want
                if extra == 0:
                    collected = b''.join(self.input)
                    self.input = []
                else:
                    input = self.input
                    self.input = [input[-1][-extra:]]
                    input[-1] = input[-1][:-extra]
                    collected = b''.join(input)

                self.got = extra

                if self.getting_size:
                    # we were recieving the message size
                    assert self.want == 4
                    self.want = unpack(">I", collected)[0]
                    self.getting_size = False
                else:
                    self.want = 4
                    self.getting_size = True
                    self.message_received(collected)
            except Exception:
                logger.exception("data_received %s %s %s",
                                 self.want, self.got, self.getting_size)


    def pause_writing(self):
        import sys; print("PAUSE", file=sys.stderr)
        self.paused.append(1)

    def resume_writing(self):
        import sys; print("RESUME_WRITING", file=sys.stderr)
        paused = self.paused
        del paused[:]
        output = self.output
        writelines = self.transport.writelines
        from struct import pack
        while output and not paused:
            message = output.pop(0)
            if isinstance(message, bytes):
                writelines((pack(">I", len(message)), message))
            else:
                data = message
                for message in data:
                    writelines((pack(">I", len(message)), message))
                    if paused: # paused again. Put iter back.
                        output.insert(0, data)
                        break

class EchoServerProtocol(Base):

    def connection_made(self, transport):
        Base.connection_made(self, transport)
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        sys.stdout.flush()
        self._write(b'SERVER')

    def message_received(self, message):
        self._write(b'RESPOND ' + message)

    def connection_lost(self, exc):
        print('The client closed the connection')
        sys.stdout.flush()

def run_server(queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain('cert.pem', 'key.pem')
    context.check_hostname = False

    coro = loop.create_server(
        EchoServerProtocol, '127.0.0.1', 8888, ssl=context)
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

class EchoClientProtocol(Base):

    def __init__(self, loop):
        Base.__init__(self)
        self.loop = loop

        self.messages = [
            (b'CLIENT',),
            (b'REGISTER xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
             b'LAST TRANSACTION xxxxxxxxxxxxxxxxxxxxxxxxxx'),
            ]

    def message_received(self, data):
        print('Message received: {!r}'.format(data.decode()))
        sys.stdout.flush()
        if self.messages:
            for m in self.messages.pop(0):
                self._write(m)
                print('Client sent: {!r}'.format(m))

        else:
            self.close()

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

import socket, struct
for i in range(20):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER,
                 struct.pack('ii', 1, 0))
    s.connect(('127.0.0.1', 8888))
    s.close()

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

coro = loop.create_connection(lambda: EchoClientProtocol(loop),
                              '127.0.0.1', 8888, ssl=context)
asyncio.async(coro, loop=loop)
loop.run_forever()

print('Done')

loop.close()
