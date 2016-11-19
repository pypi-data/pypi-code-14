import importlib
import rethinkdb as r
import aiohttp_autoreload
import brink.handlers
import brink.db
from aiohttp import web


def __print(message):
    print("==> %s" % message)


def __resolve_func(func_string):
    module_name, func_name = func_string.rsplit(".", 1)
    module = importlib.import_module(module_name)
    func = getattr(module, func_name)

    if not func:
        raise ImportError(name=func_name, path=func_string)

    return func


def __add_routes(app, urls):
    for (method, route, handler) in urls:
        handler_wrapper = brink.handlers.__ws_handler_wrapper if method == "WS" \
            else brink.handlers.__handler_wrapper

        handler_func = handler_wrapper(__resolve_func(handler))

        if method == "GET" or method == "WS":
            app.router.add_get(route, handler_func)
        elif method == "POST":
            app.router.add_post(route, handler_func)
        elif method == "PUT":
            app.router.add_put(route, handler_func)
        elif method == "PATCH":
            app.router.add_patch(route, handler_func)
        elif method == "DELETE":
            app.router.add_delete(route, handler_func)


def run(settings, urls):
    app = web.Application(middlewares=[m for m in settings.MIDDLEWARE])
    __add_routes(app, urls)
    brink.db.conn.setup(settings.RETHINKDB_CONFIG)
    aiohttp_autoreload.start()
    web.run_app(app, port=8888)

