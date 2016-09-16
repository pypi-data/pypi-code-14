from cpy2py.kernel import kernel_state


def clone_funcmeta(real_func, wrap_func):
    wrap_func.__wrapped__ = real_func
    for attribute in (
            '__doc__',
            '__signature__', '__defaults__',
            '__name__', '__module__',
            '__qualname__', '__annotations__'
    ):
        try:
            setattr(wrap_func, attribute, getattr(real_func, attribute))
        except AttributeError:
            if attribute in ('__name__', '__module__'):
                raise TypeError('Unable to inherit __module__.__name__ from %r to %r' % (real_func, wrap))


def twinfunction(twinterpreter_id, lazy=False):
    def decorator(func):
        if kernel_state.is_twinterpreter(twinterpreter_id):
            return func
        elif lazy:
            def proxy(*args, **kwargs):
                kernel_state.get_kernel(twinterpreter_id).dispatch_call(proxy, *args, **kwargs)
        else:
            kernel = kernel_state.get_kernel(twinterpreter_id)

            def proxy(*args, **kwargs):
                kernel.dispatch_call(proxy, *args, **kwargs)
        clone_funcmeta(func, proxy)
        return proxy
    return decorator
