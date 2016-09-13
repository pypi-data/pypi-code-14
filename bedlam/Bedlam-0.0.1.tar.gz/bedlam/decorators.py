from functools import partial

from bedlam.cache import register_route


def route(method, uri_pattern):

    def wrap(f):
        register_route(method, uri_pattern, f)
        return f

    return wrap


get = partial(route, 'GET')
post = partial(route, 'POST')
put = partial(route, 'PUT')
delete = partial(route, 'DELETE')
