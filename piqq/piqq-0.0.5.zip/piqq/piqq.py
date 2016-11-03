import asyncio
import functools
import threading
import json

import aioamqp

from piqq import log
from .exceptions import ConnectException


class Piqq(object):
    def __init__(self, addr, port, user, password, vhost='/', loop=None):
        self.connection_params = {'login': user, 'password': password, 'host': addr, 'port': port, 'virtualhost': vhost}
        if loop is not None:
            self.event_loop = loop
        else:
            try:
                self.event_loop = asyncio.get_event_loop()
            except RuntimeError:
                self.event_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.event_loop)

        self.max_reconnect_count = 0
        self.transport = None
        self.protocol = None

        self.default_channel = None
        self.receivers = list()

    def _error_callback(self, exception):
        log.error("AMQP exception ocurred: %r" % exception)

    async def _on_message_callback(self, channel, body, envelope, properties):
        for receiver in self.receivers:
            if envelope.routing_key in receiver.get_routing_keys():
                callbacks = dict()

                callbacks['nack'] = lambda: asyncio.run_coroutine_threadsafe(
                    channel.basic_client_nack(envelope.delivery_tag, requeue=False),
                    self.event_loop)

                callbacks['ack'] = lambda: asyncio.run_coroutine_threadsafe(
                    channel.basic_client_ack(envelope.delivery_tag),
                    self.event_loop)

                callbacks['pub'] = lambda *args, **kwargs: asyncio.run_coroutine_threadsafe(
                    self._publish(*args, **kwargs),
                    self.event_loop)

                # decode
                if properties.content_type is not None:
                    encoding = 'utf-8' if properties.content_encoding is None else properties.content_encoding

                    if properties.content_type == 'text/plain':
                        body = body.decode(encoding)
                    elif properties.content_type == 'application/json':
                        body = json.loads(body.decode(encoding))

                self.event_loop.run_in_executor(None, functools.partial(receiver.on_mq_message, channel, body, envelope,
                                                                        properties, callbacks))

    async def _connect(self):
        try_count = 0
        connected = False

        while not connected:
            try:
                self.transport, self.protocol = await aioamqp.connect(**self.connection_params,
                                                                      on_error=self._error_callback)
                log.info("Connected to %s:%d!" % (self.connection_params['host'], self.connection_params['port']))
                connected = True
            except OSError:
                log.error("AMQP connection refused")
                if try_count >= self.max_reconnect_count:
                    raise ConnectException("Connection refused")
                else:
                    log.error("Try (%d) to reconnect after 3s..." % try_count)
                    try_count += 1
                    await asyncio.sleep(3)

    async def _close(self):
        log.info("Initiating connection close...")
        await self.protocol.close()
        self.transport.close()

    async def _init_commands(self):
        log.info("Collecting recevers...")
        for receiver in self.receivers:
            await self._register_command(receiver)

    async def _register_command(self, command_class):
        # Declare channel for each receiver
        channel = await self.protocol.channel()

        # Setup QOS
        if command_class.get_qos_size() is not None:
            await channel.basic_qos(prefetch_count=command_class.get_qos_size(), prefetch_size=0,
                                    connection_global=False)

        # Declare exchange
        await channel.exchange(**command_class.get_exchange())

        # Declare queue
        result = await channel.queue(**command_class.get_queue(), auto_delete=False)
        queue_name = result['queue']

        # Bind keys to queue
        for binding_key in command_class.get_routing_keys():
            await channel.queue_bind(
                exchange_name=command_class.get_exchange()['exchange_name'],
                queue_name=queue_name,
                routing_key=binding_key
            )

        # Consuming
        log.info("Consuming command %s" % command_class)
        await channel.basic_consume(self._on_message_callback, queue_name=queue_name)

    async def _get_channel(self):
        if self.default_channel is None or not self.default_channel.is_open:
            self.default_channel = await self.protocol.channel()

        return self.default_channel

    async def _publish(self, exchange, routing_key, body, channel=None, delivery_mode=1, serialize_as='text'):
        # get channel
        if channel is None:
            channel = await self._get_channel()

        # Declare exchange
        await channel.exchange(**exchange)

        # Set properties
        properties = {'delivery_mode': delivery_mode}
        if serialize_as == 'text':
            properties['content_type'] = 'text/plain'
            properties['content_encoding'] = 'utf-8'
        elif serialize_as == 'json':
            properties['content_type'] = 'application/json'
            properties['content_encoding'] = 'utf-8'
            body = json.dumps(body)

        await channel.basic_publish(body,
                                    exchange_name=exchange['exchange_name'],
                                    routing_key=routing_key,
                                    properties=properties)

    def pub(self, *args, **kwargs):
        asyncio.run_coroutine_threadsafe(self._publish(*args, **kwargs), self.event_loop)

    def add_command(self, command_class):
        self.receivers.append(command_class)

    def close(self):
        asyncio.run_coroutine_threadsafe(self._close(), self.event_loop)

    def run_exclusive(self, max_try=0):
        self.max_reconnect_count = max_try
        self.event_loop.run_until_complete(self._connect())
        self.event_loop.run_until_complete(self._init_commands())
        log.info("Consuming... Press Ctrl+C to exit")
        self.event_loop.run_forever()

    def run_silently(self, max_try=0):
        self.max_reconnect_count = max_try
        thread = threading.Thread(target=self.event_loop.run_forever, name="PIQQ event loop", daemon=True)
        self.event_loop.run_until_complete(self._connect())
        self.event_loop.run_until_complete(self._init_commands())
        thread.start()
