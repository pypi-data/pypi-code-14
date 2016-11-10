import functools

import bson
import falcon
from pyfunk import combinators

from pylib import lib
from pylib.security import tokens


@combinators.curry
def setup_hooks(pre, post, handler):
    """
    Setup the pre and post processors for the given handler.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig setup_hooks :: [Hook] -> [Hook] -> (* -> _) ->(* -> _)
    """
    handler = functools.reduce(lambda x, y: y(x), reversed(list(map(falcon.before, pre))), handler)
    handler = functools.reduce(lambda x, y: y(x), reversed(list(map(falcon.after, post))), handler)
    return handler


@combinators.curry
def decorate_handler(pre, post, method, api, fn):
    """
    Creates a handler for the given method using the given function.
    It also sets up the given hooks for the function before registering
    it.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig decorate_handler :: [Hook] -> [Hook] -> Str -> FalconApi -> (* -> _) -> _
    """
    allpre = api.pre + pre
    allpost = api.post + post
    fn = setup_hooks(allpre, allpost, fn)
    lib.attach_method(api.resource, method, fn)


def int_id_converter(idname):
    """
    Creates a hook for casting the idname parameter in the url of an api
    to an int.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig int_id_converter :: Str -> Hook
    """
    def hook(req, resp, res, params):
        try:
            params[idname] = int(params[idname])
        except ValueError:
            falcon.HTTPBadReuest('Invalid id', 'ID is not valid')
    return hook


def object_id_converter(idname):
    """
    Creates a hook for casting the idname parameter in the url of an api
    to an object id.
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig object_id_converter :: Str -> Hook
    """
    def hook(req, resp, res, params):
        try:
            params[idname] = bson.ObjectId(params[idname])
        except ValueError:
            falcon.HTTPBadReuest('Invalid id', 'ID is not valid')
    return hook


def cookie_fixer(key, secure=False):
    """
    Creates a pro hook for attaching a value to a cookie using the given key
    from the dict. If secure mode is turned off, the cookies values can be
    sent over normal HTTP.
    @type Hook => (Request -> Response -> Resource -> _)
    @sig cookie_fixer :: Str -> Hook
    """
    def hook(req, resp, res):
        resp.set_cookie(key, req.context['result'][key], secure=secure)
    return hook


def token_decoder(tokenkey, secret, excclass, algorithm='HS256'):
    """
    Creates a pre hook for decoding and retrieving a value from a cookie from `tokenkey`
    and decoding it using `secret` and `algorithm`. It uses the token module(which uses
    jwt) for decoding. excclass is called if the decoding fails with the instance of the
    exception, with the return values raised as an exception.
    @DecodeFn => (Exception -> _)
    @type Hook => (Request -> Response -> Resource -> {Str: Str} -> _)
    @sig token_decoder :: Str ->  Str -> DecodeFn ->Hook
    """
    def hook(req, resp, res, params):
        try:
            val = tokens.decode(req.cookies[tokenkey], secret, algorithm)
            req.context[tokenkey] = val
        except Exception as e:
            excclass(e)
    return hook
