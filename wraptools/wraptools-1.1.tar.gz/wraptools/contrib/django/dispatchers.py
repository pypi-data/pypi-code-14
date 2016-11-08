from wraptools.dispatch import dispatcher


@dispatcher
def is_authenticated(request, *args, **kwargs):
    """ Dispatcher for django views functions to dispatch to authentication views
    """
    return request.user.is_authenticated


def method(method_name):
    """ Dispatcher to route when request.method is same with :param method_name:
    """
    @dispatcher
    def _dispatcher(request, *args, **kwargs):
        return request.method == method_name
    return _dispatcher


method_get = method("GET")
method_post = method("POST")
method_put = method("PUT")
method_delete = method("DELETE")


def has_param(param_name):
    """ Dispatcher to route when request.GET or request.POST has :param param_name: value.
    """
    @dispatcher
    def _dispatcher(request, *args, **kwargs):
        return param_name in request.GET or param_name in request.POST
    return _dispatcher
