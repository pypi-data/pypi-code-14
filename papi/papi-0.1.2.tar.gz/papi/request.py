from urllib.parse import parse_qsl
from papi.mime import parse_http_accept, parse_mime_type
import papi.fp as fp
from functools import partial

def parse_request_middleware(application):
    def wrapped(environ, start_response):
        request = parse_request(environ)
        new_environ = fp.assoc('request', request, environ)
        return application(new_environ, start_response)
    return wrapped

def parse_request(environ):
    return {
        'path': parse_path(environ['PATH_INFO']),
        'accept': parse_http_accept(
            environ.get('HTTP_ACCEPT', 'application/json'),
            sort=True),
        'content_type': parse_mime_type(
            environ.get('CONTENT_TYPE', 'application/json')),
        'headers': get_headers(environ),
        'method': environ['REQUEST_METHOD'],
        'query': dict(parse_qsl(environ['QUERY_STRING'], keep_blank_values=True)),
        'input': environ.get('wsgi.input'),
    }

def get_headers(environ):
    def convert_header_name(hname):
        return fp.chain(
            '-'.join,
            partial(map, str.capitalize),
            lambda x: x.split('_'),
            lambda x: x[len('HTTP_'):])(hname)
    headers = (
            (convert_header_name(name), val)
            for name, val
            in dict(environ).items()
            if name.startswith('HTTP_')
        )
    return dict(headers)
            
def parse_path(s, skip_trailing_slash=True):
    parts = s.strip().split('/')
    if len(parts) > 0 and parts[0] == '':
        parts = parts[1:]
    if parts == []:
        return ()
    if skip_trailing_slash and parts[-1] == '':
        parts = parts[:-1]
    return tuple(parts)
