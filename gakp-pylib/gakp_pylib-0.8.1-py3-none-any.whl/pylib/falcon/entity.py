import re
from pyfunk.combinators import curry
from pylib.falcon.hooks import add_handler
from pylib.falcon.middleware import response
from pylib.lib import merge_dict, english_index
from pylib.marshmallow import load

paramregex = re.compile(r'\{(\w+)\}')


@curry
def get_parameter(at, url):
    """
    Gets the relative parameter from the url according to `at`.
    @sig get_parameter :: Str | Int -> Str -> Str
    """
    params = [m.group(1) for m in [paramregex.match(path) for path in url.split('/')]]
    return english_index(at, params)

get_last_parameter = get_parameter('last')


def read(api, pre=[], post=[]):
    """
    Sets the api handler for GET requests on the falcon api object. Unlike
    collection.search this handles per entity requests using the parameter
    defined in the path of the api.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @type ReadFn => (Int | ObjectId -> * -> a)
    @sig read :: FalconApi -> [Hook] -> [Hook] -> (ReadFn -> ReadFn)
    """
    def decorator(f):
        def get(res, req, resp, **kwargs):
            entityid = kwargs.pop(get_last_parameter(api.path))
            readentity = f(entityid, merge_dict(kwargs, req.context))
            response(resp, api.schema, readentity)

        add_handler(pre, post, 'on_get', api, get)
        return f
    return decorator


def update(api, pre=[], post=[]):
    """
    Sets the api handler for PUT requests on the falcon api object.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @type UpdateFn => (Int | ObjectId -> a -> * -> a)
    @sig update :: FalconApi -> [Hook] -> [Hook] -> (UpdateFn -> UpdateFn)
    """
    def decorator(f):
        def edit(res, req, resp, **kwargs):
            entityid = kwargs.pop(get_last_parameter(api.path))
            reqentity = load(api.schema,  dict(req.params))

            newentity = f(entityid, reqentity, merge_dict(kwargs, req.context))
            response(resp, api.schema, newentity)

        add_handler(pre, post, 'on_put', api, edit)
        return f
    return decorator


def delete(api, pre=[], post=[]):
    """
    Sets the api handler for DELETE requests on the falcon api object.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @type DeleteFn => (Int | ObjectId -> * -> a)
    @sig delete :: FalconApi -> [Hook] -> [Hook] -> (DeleteFn -> DeleteFn)
    """
    def decorator(f):
        def remove(res, req, resp, **kwargs):
            entityid = kwargs.pop(get_last_parameter(api.path))
            oldentity = f(entityid, merge_dict(kwargs, req.context))
            response(resp, api.schema, oldentity)

        add_handler(pre, post, 'on_delete', api, remove)
        return f
    return decorator
