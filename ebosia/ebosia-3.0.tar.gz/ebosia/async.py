import asyncio
import logging
import urllib.parse

import aioamqp

import ebosia
import ebosia.events

LOGGER = logging.getLogger(__name__)

class ClosedConnection(Exception):
    pass

class Connection(): # pylint: disable=too-many-instance-attributes
    def __init__(self, url, on_error=None, on_reconnect=None, heartbeat=60):
        parts = urllib.parse.urlparse(url)
        if parts.scheme != 'amqp':
            raise Exception("Only 'amqp' is supported for the connection scheme at this time")

        self.channel        = None
        self.heartbeat      = heartbeat
        self.on_error       = on_error
        self.on_reconnect   = on_reconnect
        self.parts          = parts
        self.protocol       = None
        self.reconnect_lock = asyncio.Lock()
        self.transport      = None


    @asyncio.coroutine
    def error_callback(self, error):
        LOGGER.warning("Error in connection to eventbus: %s", error)
        if self.on_error:
            yield from self.on_error(error)
        if self.reconnect_lock.locked():
            LOGGER.debug("Not reconnecting, the reconnect lock is engaged")
        else:
            asyncio.async(self.reconnect()) # pylint: disable=deprecated-method


    @asyncio.coroutine
    def reconnect(self):
        with (yield from self.reconnect_lock):
            wait_time = 0.1
            while True:
                try:
                    yield from self.connect()
                    if self.on_reconnect:
                        yield from self.on_reconnect()
                    return
                except OSError as e:
                    LOGGER.warning("Unable to reconnect: %s", e)
                    yield from asyncio.sleep(wait_time)
                    wait_time = min(3.0, wait_time * 1.5)

    @asyncio.coroutine
    def connect(self):
        try:
            transport, protocol = yield from aioamqp.connect(
                host        = self.parts.hostname,
                port        = self.parts.port,
                login       = self.parts.username,
                password    = self.parts.password,
                virtualhost = self.parts.path or '/',
                insist      = True,
                on_error    = self.error_callback,
                heartbeat   = self.heartbeat,
            )
        except aioamqp.AmqpClosedConnection:
            raise ClosedConnection

        self.channel   = yield from protocol.channel()
        self.protocol  = protocol
        self.transport = transport

@asyncio.coroutine
def declare_exchange(connection=None):
    connection = connection or ebosia.get()
    exchange = yield from connection.channel.exchange(
        'eventbus',
        'topic',
        passive         = False,
        durable         = False,
        auto_delete     = False,
        no_wait         = False,
    )
    return exchange

def _sync_to_async(callback):
    def _on_done(result):
        if result.exception():
            raise result.exception()

    def _sync_callback(event):
        loop = asyncio.get_event_loop()
        coro = loop.create_task(callback(event))
        coro.add_done_callback(_on_done)
        loop.run_until_complete(coro)
    return _sync_callback

@asyncio.coroutine
def subscribe(topic, callback, connection=None):
    connection = connection or ebosia.get()
    # If we are testing the connection we receive will actually be an in-memory
    # kombu connection. That's fine, we just need to do some translation
    if getattr(connection, 'PRETENDING_TO_BE_ASYNC', None):
        return connection.subscribe(topic, _sync_to_async(callback))

    @asyncio.coroutine
    def on_message(channel, body, envelope, properties): # pylint: disable=unused-argument
        event = ebosia.events.from_aioamqp(body, envelope, properties)
        LOGGER.debug("Received %s", event)
        yield from callback(event)

    yield from declare_exchange(connection)
    result = yield from connection.channel.queue_declare(
        queue_name  = '',
        passive     = False,
        durable     = False,
        exclusive   = True,
        no_wait     = False,
    )
    yield from connection.channel.queue_bind(
        queue_name      = result['queue'],
        exchange_name   = 'eventbus',
        routing_key     = topic,
        no_wait         = False,
    )
    yield from connection.channel.basic_consume(on_message, queue_name=result['queue'], no_ack=True)

@asyncio.coroutine
def connect(url, on_error=None, on_reconnect=None, heartbeat=60):
    connection = Connection(url, on_error, on_reconnect=on_reconnect, heartbeat=heartbeat)
    yield from connection.connect()
    ebosia.store(connection)
    return connection

@asyncio.coroutine
def disconnect(connection=None):
    connection = connection or ebosia.get()
    yield from connection.protocol.close()
    connection.transport.close()
