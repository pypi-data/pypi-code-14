from functools import wraps
from django.http import Http404
from django.http import HttpResponse

from .utils import function_from_string

def _return_blank_or_raise_404(is_ajax):
    """
    Return empty string '' in case of ajax requests and raise 404 in case
    of non-ajax requests.
    """
    if is_ajax:
        return HttpResponse('')
    else:
        raise Http404


def quick(config, mysterious=None, only_authenticated=None):
    """
    Decides whether this user is allowed to access this view or not.

    :param config - Decides if the setting is on globally.
    :callable_name - The function which will return the list of users which are
                     eligible for proceeding further after this action.
    """

    def decorator(func):

        @wraps(func)
        def _quick(request, *args, **kwargs):
            # Check if the request is ajax.
            is_ajax = request.is_ajax()

            # Check if the config is available globally and return '' or raise
            # 404 as per the nature of the request.
            if not config:
                return _return_blank_or_raise_404(is_ajax)
            callable_name = None
            _only_authenticated = None

            if mysterious is not None:
                if type(mysterious) == bool:
                    _only_authenticated = mysterious
                else:
                    callable_name = mysterious
            elif only_authenticated is not None:
                _only_authenticated = only_authenticated

            user = request.user
            if callable_name is None:
                if (_only_authenticated is not None and
                        _only_authenticated and
                        not user.is_authenticated()):
                    return _return_blank_or_raise_404(is_ajax)
                else:
                    return func(request, *args, **kwargs)
            else:
                if not user.is_authenticated():
                    return _return_blank_or_raise_404(is_ajax)
                else:
                    _callable = function_from_string(callable_name)
                    if user.id in _callable():
                        return func(request, *args, **kwargs)
                    return _return_blank_or_raise_404(is_ajax)
            return _return_blank_or_raise_404(is_ajax)
        return _quick
    return decorator
