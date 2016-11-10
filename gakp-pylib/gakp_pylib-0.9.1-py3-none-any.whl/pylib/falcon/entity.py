import re

from pyfunk import collections
from pyfunk import combinators

from pylib import lib
from pylib import marshmallow
from pylib.falcon import hooks
from pylib.falcon import middleware

paramregex = re.compile(r'\{(\w+)\}')


def get_parameters(regex, url):
    """
    Returns all the parameters in the given path, with `regex`
    describing the pattern of a parameter.
    @sig get_parameter :: RegExp -> Str -> [Str]
    """
    return [m.group(1) for m in [paramregex.match(path) for path in url.split('/')] if m is not None]


last_parameter = combinators.compose(collections.last, get_parameters)


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
            entityid = kwargs.pop(last_parameter(api.path))
            readentity = f(entityid, **lib.merge_dict(kwargs, req.context))
            req.context['result'] = readentity
            middleware.response(resp, api.schema, readentity)

        hooks.decorate_handler(pre, post, 'on_get', api, get)
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
            entityid = kwargs.pop(last_parameter(api.path))
            reqentity = marshmallow.load(api.schema,  dict(req.params))

            newentity = f(entityid, reqentity, **lib.merge_dict(kwargs, req.context))
            req.context['result'] = newentity
            middleware.response(resp, api.schema, newentity)

        hooks.decorate_handler(pre, post, 'on_put', api, edit)
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
            entityid = kwargs.pop(last_parameter(api.path))
            oldentity = f(entityid, **lib.merge_dict(kwargs, req.context))
            req.context['result'] = oldentity
            middleware.response(resp, api.schema, oldentity)

        hooks.decorate_handler(pre, post, 'on_delete', api, remove)
        return f
    return decorator
