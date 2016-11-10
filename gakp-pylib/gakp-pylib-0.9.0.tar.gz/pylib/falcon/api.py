import collections

from pyfunk import combinators

import falcon
from pylib import lib
from pylib import marshmallow
from pylib.falcon import hooks
from pylib.falcon import middleware

FalconApi = collections.namedtuple('FalconApi', ['path', 'schema', 'pre', 'post', 'resource'])


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


@combinators.curry
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
    apimiddleware = list((middleware.RequireJSON(), middleware.JSONTranslator()) + args)
    api = falcon.API(middleware=apimiddleware)
    api.set_error_serializer(middleware.json_error_serializer)
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
            entity = marshmallow.load(api.schema, dict(req.params))
            result = f(entity, **lib.merge_dict(kwargs, req.context))
            req.context['result'] = result
            middleware.response(resp, api.schema, result)

        hooks.decorate_handler(pre, post, 'on_post', api, new)
        return f
    return decorator
