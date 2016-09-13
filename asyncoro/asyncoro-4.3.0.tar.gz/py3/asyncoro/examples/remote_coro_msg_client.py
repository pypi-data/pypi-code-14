#!/usr/bin/env python

# client sends messages to a remote coroutine
# use with its server 'remote_coro_msg_server.py'

import sys, random
# import disasyncoro to use distributed version of AsynCoro
import asyncoro.disasyncoro as asyncoro

def sender(i, server_coro, coro=None):
    msg = '%d: ' % i + '-' * random.randint(100,300) + '/'
    yield server_coro.send(msg)

def create_senders(n, coro=None):
    # if server is in remote network, add it; set 'stream_send' to
    # True for streaming messages to it
    # yield scheduler.peer('remote.peer.ip', stream_send=True)
    server_coro = yield asyncoro.Coro.locate('server_coro')
    print('server is at %s' % server_coro.location)
    for i in range(n):
        asyncoro.Coro(sender, i, server_coro)

asyncoro.logger.setLevel(asyncoro.Logger.DEBUG)
# scheduler = asyncoro.AsynCoro(secret='key')
asyncoro.Coro(create_senders, 10 if len(sys.argv) < 2 else int(sys.argv[1]))
