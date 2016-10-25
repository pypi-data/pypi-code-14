from urllib.parse import parse_qsl
import papi.fp as fp

def method_override_middleware(application):
    def wrapped(environ, start_response):
        query = dict(
                    parse_qsl(
                        environ['QUERY_STRING'],
                        keep_blank_values=True))
        method_override = \
            fp.prop('_method', query) or \
            fp.prop('HTTP_X_METHOD_OVERRIDE', environ) or \
            fp.prop('REQUEST_METHOD', environ)
        new_environ = fp.assoc('REQUEST_METHOD', method_override, environ)
        return application(new_environ, start_response)
    return wrapped
