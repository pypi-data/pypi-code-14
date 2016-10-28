from pylib.falcon.hooks import add_handler
from pylib.falcon.middleware import response
from pylib.lib import merge_dict
from pylib.marshmallow import load


def find(api, pre=[], post=[]):
    """
    Sets the api handler for GET requests on the falcon api object.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @type SearchFn => (Str -> * -> [a])
    @sig find :: FalconApi -> [Hook] -> [Hook] -> (SearchFn -> SearchFn)
    """
    def decorator(f):
        def findin(res, req, resp, **kwargs):
            query = req.get_param('query')
            entities = f(query, **merge_dict(kwargs, req.context))
            assert isinstance(entities, list)
            response(resp, api.schema, entities, many=True)

        add_handler(pre, post, 'on_get', api, findin)
        return f
    return decorator


def create(api, pre=[], post=[]):
    """
    Sets the api handler for POST requests on the falcon api object.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @type CreateFn => (a-> * -> Int | Str)
    @sig create :: FalconApi -> [Hook] -> [Hook] -> (CreateFn -> CreateFn)
    """
    def decorator(f):
        def new(res, req, resp, **kwargs):
            entity = load(api.schema, dict(req.params))
            entityid = f(entity, **merge_dict(kwargs, req.context))
            assert isinstance(entityid, (str, int))
            response(resp, api.schema, dict(id=entityid))

        add_handler(pre, post, 'on_post', api, new)
        return f
    return decorator
