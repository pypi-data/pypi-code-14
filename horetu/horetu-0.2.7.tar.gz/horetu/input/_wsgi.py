from .types import Input
from . import lib

@Input
def wsgi(f, environ):
    from webob import Request
    return _wsgi(f, Request(environ))

def _wsgi(f, req):
    pos = req.path_info.split('/')[1:]
    x = lib.getsection(False, f, pos)

    def _flatten(multidict):
        for k in multidict:
            for v in multidict.getall(k):
                yield k, v
    return {
        'func': x.func,
        'section': x.section,
        'positionals': pos[len(x.section):],
        'flags': list(_flatten(req.GET)),
    }
