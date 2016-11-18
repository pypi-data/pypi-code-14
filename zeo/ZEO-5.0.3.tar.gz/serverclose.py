import asyncio
import socket

class Protocol(asyncio.Protocol):

    def connection_made(*a):
        pass

    connection_lost = data_received = connection_made

loop = asyncio.get_event_loop()

def done(future):
    if not isinstance(future, asyncio.Future):
        future = asyncio.async(future, loop=loop)

    def do(func):
        future.add_done_callback(func)
        return func

    return do

@done(loop.create_server(Protocol, '127.0.0.1', 0, reuse_address=True))
def listening(f):
    global server
    server = f.result()
    [ss] = server.sockets

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ss.getsockname())
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2.connect(ss.getsockname())

    def close():
        print("closing")
        server.close()

        @done(server.wait_closed())
        def closed(f):
            loop.call_soon(loop.stop)

    loop.call_later(1, close)

loop.run_forever()
loop.close()

