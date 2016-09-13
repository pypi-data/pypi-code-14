from bedlam.errors import PayloadError


def require(*keys):
    def wraps(f):
        def wrapper(req, *a, **kw):
            for k in keys:
                if k not in req.body:
                    raise PayloadError
            return f(req, *a, **kw)
        return wrapper
    return wraps


def allow(*keys):
    def wraps(f):
        def wrapper(req, *a, **kw):
            for k, _ in req.body:
                if k not in keys:
                    raise PayloadError
            return f(req, *a, **kw)
        return wrapper
    return wraps
