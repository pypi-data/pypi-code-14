from functools import partial, reduce
from operator import add
import werkzeug.test
from qubit.wsgiapp import app

__all__ = ['client', 'request', 'get']

client = werkzeug.test.Client(app)
environ_overrides = {'REMOTE_ADDR': '127.0.0.1'}


def request(*args, **kwargs):
    resp = partial(client.open,
                   environ_overrides=environ_overrides,
                   content_type='application/json')(*args, **kwargs)[0]
    return reduce(add, map(bytes, resp)).decode()


def get(*args, **kwargs):
    resp = client.open(environ_overrides=environ_overrides,
                       *args, **kwargs)[0]
    return reduce(add, map(bytes, resp)).decode()
