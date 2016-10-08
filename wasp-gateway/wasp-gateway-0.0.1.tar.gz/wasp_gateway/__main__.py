import asyncio

import uvloop

from wasp_gateway.core import run
from wasp_gateway.http.dispatcher import HTTPDispatcher
from wasp_gateway.http.resolver import DictServiceResolver


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    resolver = DictServiceResolver({
        'foo': 'http://localhost:8081',
        'bar': 'http://localhost:8082',
    })
    dispatcher = HTTPDispatcher(resolver)
    run(dispatcher, loop=asyncio.get_event_loop())
