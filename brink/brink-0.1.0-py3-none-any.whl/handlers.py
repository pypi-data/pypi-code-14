from aiohttp import web
from cerberus import Validator
from brink.serialization import json_dumps
from brink.exceptions import HTTPBadRequest


class WebSocketResponse(web.WebSocketResponse):
    def send_json(self, json, *args, **kwargs):
        super().send_json(json, *args, dumps=json_dumps, **kwargs)


def __handler_wrapper(handler):
    async def new_handler(request):
        status, data = await handler(request)
        return web.json_response(data, status=status, dumps=json_dumps)
    return new_handler


def __ws_handler_wrapper(handler):
    async def new_handler(request):
        ws = WebSocketResponse()
        await ws.prepare(request)
        await handler(request, ws)
        return ws
    return new_handler


def handle_model(cls, validate=True):
    v = Validator(cls.schema)

    def decorator(handler):
        async def new_handler(request):
            body = await request.json()

            if validate and not v.validate(body):
                raise HTTPBadRequest(text=json_dumps(v.errors), content_type="application/json")

            model = cls(**body)
            return await handler(request, model)
        return new_handler
    return decorator
