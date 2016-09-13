import functools

import ujson

from bedlam.cache import map_route
from bedlam.errors import BedlamError
from bedlam.request import Request


def error_handler(f):
    @functools.wraps(f)
    def wrap(environ, start_response):
        try:
            return f(environ, start_response)
        except BedlamError as err:
            return err.handle(start_response)
        except:
            return BedlamError.handle(start_response)

    return wrap


@error_handler
def run(environ, start_response):
    request = Request(environ)

    handler, groups, named_groups = map_route(request.method, request.path)
    data = handler(request, *groups, **named_groups)
    data = ujson.dumps(data)

    status = '200'
    response_headers = [
        ('content-type', 'application/json',),
        ('content-length', str(len(data)),),
    ]

    start_response(status, response_headers)
    return iter([data])
