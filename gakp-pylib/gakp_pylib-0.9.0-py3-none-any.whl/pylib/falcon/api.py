import falcon
from collections import namedtuple
from pylib.falcon.hooks import add_handler
from pylib.falcon.middleware import (
    json_error_serializer, response,
    JSONTranslator, RequireJSON
)
from pylib.lib import merge_dict
from pylib.marshmallow import load
from pyfunk.combinators import curry

FalconApi = namedtuple('FalconApi', ['path', 'schema', 'pre', 'post', 'resource'])


class FalconResource(object):
    """
    Instances of this class are used to register url to the api.
    Request handlers in each of the abstractions are attached to the
    instance.
    """
    pass


def create_api(path, schema, pre=[], post=[]):
    """
    Create a falcon api object. The API object holds the path and pre/post
    processors of the API's events. The schema is a marshmallow schema object
    which is one of the preprocessors. The other pre/post processors are basically
    falcon before/after handlers respectively.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig create_api :: Str -> Schema -> [Hook] -> [Hook] -> FalconApi
    """
    return FalconApi(path, schema, pre, post, FalconResource())


@curry
def register(api, fapi):
    """
    Link the FalconApi object and the actual falcon API instance.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig register :: FalconApi -> API -> _
    """
    fapi.add_route(api.path, api.resource)


def create_falcon_api(*args):
    """
    Creates a falcon.API with JSON as it's transport mechanism.
    @sig create_falcon_api :: Middleware... -> API
    """
    middleware = list((RequireJSON(), JSONTranslator()) + args)
    api = falcon.API(middleware=middleware)
    api.set_error_serializer(json_error_serializer)
    return api


def pure(api, pre=[], post=[]):
    """
    Sets the api handler for POST requests on the falcon api object.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @type PureFn => (a-> * -> a)
    @sig create :: FalconApi -> [Hook] -> [Hook] -> (PureFn -> PureFn)
    """
    def decorator(f):
        def new(res, req, resp, **kwargs):
            entity = load(api.schema, dict(req.params))
            result = f(entity, **merge_dict(kwargs, req.context))
            req.context['result'] = result
            response(resp, api.schema, result)

        add_handler(pre, post, 'on_post', api, new)
        return f
    return decorator
