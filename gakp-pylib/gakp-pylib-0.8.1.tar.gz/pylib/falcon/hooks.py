import falcon
import functools
from bson import ObjectId
from pyfunk.combinators import curry
from pylib.lib import attach_method


@curry
def setup_hooks(pre, post, handler):
    """
    Setup the pre and post processors for the given handler.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig setup_hooks :: [Hook] -> [Hook] -> (* -> _) ->(* -> _)
    """
    handler = functools.reduce(lambda x, y: y(x), map(falcon.before, pre), handler)
    handler = functools.reduce(lambda x, y: y(x), map(falcon.after, post), handler)
    return handler


@curry
def add_handler(pre, post, method, api, fn):
    """
    Creates a handler for the given method using the given function.
    It also sets up the given hooks for the function before registering
    it.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig add_handler :: [Hook] -> [Hook] -> Str -> FalconApi -> (* -> _) -> _
    """
    allpre = api.pre + pre
    allpost = api.post + post
    fn = setup_hooks(allpre, allpost, fn)
    attach_method(api.resource, method, fn)


def int_id_hook(idname):
    """
    Creates a hook for casting the idname parameter in the url of an api
    to an int.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig int_id_hook :: Str -> Hook
    """
    def hook(req, resp, res, params):
        try:
            params[idname] = int(params[idname])
        except ValueError:
            falcon.HTTPBadReuest('Invalid id', 'ID is not valid')
    return hook


def object_id_hook(idname):
    """
    Creates a hook for casting the idname parameter in the url of an api
    to an object id.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig object_id_hook :: Str -> Hook
    """
    def hook(req, resp, res, params):
        try:
            params[idname] = ObjectId(params[idname])
        except ValueError:
            falcon.HTTPBadReuest('Invalid id', 'ID is not valid')
    return hook
