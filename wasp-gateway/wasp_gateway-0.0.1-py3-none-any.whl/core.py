import asyncio
import re
import uuid

import aiohttp
import aiohttp.server

from wasp_gateway.http.dispatcher import HTTPDispatcher


class GatewayRequestHandler(aiohttp.server.ServerHttpProtocol):
    routing_re = re.compile(r'^/(?P<service>[^/]+)(?P<path>/.*)$',
                            flags=re.IGNORECASE | re.DOTALL)

    def __init__(self, dispatcher: HTTPDispatcher, **kwargs):
        self.dispatcher = dispatcher
        super().__init__(**kwargs)

    async def handle_request(self,
                             message: aiohttp.protocol.RawRequestMessage,
                             payload: aiohttp.streams.FlowControlStreamReader):
        routing_match = self.routing_re.match(message.path)
        if not routing_match:
            raise aiohttp.HttpProcessingError(code=404,
                                              message='Route not found')

        service = routing_match.group('service')
        path = routing_match.group('path')

        # context ids to trace requests in the system
        # TODO: send these to a centralized service?
        #       could be a good feature to have an aggregation
        #       center.
        message.headers['X-REQUEST-CONTEXT'] = str(uuid.uuid4())

        # TODO: need to see if we can abstract away some of this lower level
        #       stuff for easy to create other dispatcher options. With HTTP
        #       it's ideal to just stream the input through to the remote
        #       service, but with the BUS impl this will likely look
        #       substantially different...
        await self.dispatcher.dispatch(service, path, message, payload,
                                       self.writer)


def run(dispatcher, *, loop=None, host: str='0.0.0.0', port: int=8080):
    loop = loop or asyncio.get_event_loop()
    f = loop.create_server(lambda: GatewayRequestHandler(dispatcher),
                           host, port)
    srv = loop.run_until_complete(f)
    print('Serving on: http://{}:{}'.format(*srv.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
