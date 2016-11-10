import bson

from pylib import lib
from pylib import marshmallow
from pylib.falcon import hooks
from pylib.falcon import middleware


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
            entities = f(query, **lib.merge_dict(kwargs, req.context))
            assert isinstance(entities, list)
            req.context['result'] = entities
            middleware.response(resp, api.schema, entities, many=True)

        hooks.decorate_handler(pre, post, 'on_get', api, findin)
        return f
    return decorator


def create(api, pre=[], post=[]):
    """
    Sets the api handler for POST requests on the falcon api object.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @type CreateFn => (a-> * -> Int | ObjectId)
    @sig create :: FalconApi -> [Hook] -> [Hook] -> (CreateFn -> CreateFn)
    """
    def decorator(f):
        def new(res, req, resp, **kwargs):
            entity = marshmallow.load(api.schema, dict(req.params))
            entityid = f(entity, **lib.merge_dict(kwargs, req.context))
            assert isinstance(entityid, (bson.ObjectId, int))
            req.context['result'] = entityid
            middleware.response(resp, api.schema, dict(id=entityid))

        hooks.decorate_handler(pre, post, 'on_post', api, new)
        return f
    return decorator
