from urllib.parse import parse_qs, quote, urlencode
import sys
import re
import http.cookies
import logging
from datetime import datetime, date
import json
from enum import Enum
from decimal import Decimal
import os.path
import posixpath
from functools import partial
from http.client import responses as http_responses
from wsgiref.headers import Headers
from unicodedata import normalize
import mimetypes
import cgi

__all__ = (
    'MultiValueDict', 'HttpError', 'HttpRequest', 'HttpResponse', 'Controller', 'Router', 'Route',
    'Application', 'static_file', 'load_controllers', 'make_simple_controllers', 'json_encode'
)

logger = logging.getLogger('peepal')


# copied from django
class MultiValueDict(dict):
    def __getitem__(self, key):
        """
        Returns the last data value for this key,
        raises KeyError if not found or it's an empty list.
        """
        list_ = super().__getitem__(key)
        try:
            return list_[-1]
        except IndexError:
            raise KeyError(key) from None

    def __setitem__(self, key, value):
        super().__setitem__(key, [value])

    def __copy__(self):
        return self.__class__([
            (k, v[:])
            for k, v in self.lists()
        ])

    def get(self, key, default=None):
        """
        Returns the last data value for the passed key. If key doesn't exist
        or value is an empty list, then default is returned.
        """
        try:
            val = self[key]
        except KeyError:
            return default
        return val

    def getlist(self, key):
        """
        Returns the list of values for the passed key. If key doesn't exist,
        then an empty list is returned.
        """
        try:
            return super().__getitem__(key)
        except KeyError:
            return []

    def setlist(self, key, list_):
        super().__setitem__(key, list_)

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def setlistdefault(self, key, default_list=None):
        if key not in self:
            if default_list is None:
                default_list = []
            self.setlist(key, default_list)
            return default_list
        return super().__getitem__(key)

    def append(self, key, value):
        """Appends an item to the internal list associated with key."""
        self.setlistdefault(key).append(value)

    def items(self):
        """
        Returns a list of (key, value) pairs, where value is the last item in
        the list associated with the key.
        """
        return [(key, value[-1]) for key, value in super().items() if value]

    def lists(self):
        """Returns a list of (key, list) pairs."""
        return [(key, value) for key, value in super().items() if value]

    def values(self):
        """Returns a list of the last value on every key list."""
        return [value[-1] for value in super().values() if value]

    def copy(self):
        """Returns a shallow copy of this object."""
        return self.__copy__()

    def update(self, *args, **kwargs):
        """
        update() extends rather than replaces existing key lists.
        Also accepts keyword args.
        """
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        if args:
            other_dict = args[0]
            if isinstance(other_dict, MultiValueDict):
                for key, value_list in other_dict.lists():
                    self.setlistdefault(key).extend(value_list)
            else:
                try:
                    for key, value in other_dict.items():
                        self.setlistdefault(key).append(value)
                except TypeError:
                    raise ValueError("MultiValueDict.update() takes either a MultiValueDict or dictionary")
        for key, value in kwargs.items():
            self.setlistdefault(key).append(value)


def get_host(environ):
    if 'HTTP_HOST' in environ:
        return environ['HTTP_HOST']
    result = environ['SERVER_NAME']
    if (environ['wsgi.url_scheme'], environ['SERVER_PORT']) not \
       in (('https', '443'), ('http', '80')):
        result += ':' + environ['SERVER_PORT']
    return result


def copyfileobj(fsrc, fdst, chunk_size=2**16):
    while True:
        buf = fsrc.read(chunk_size)
        if not buf:
            break
        fdst.write(buf)


class HttpError(Exception):
    """An exception that will turn into an HTTP error response."""

    def __init__(self, status_code, description=''):
        assert status_code >= 400, 'HttpError is meant to indicate an error, status must be greater than or equal to 400.'
        self.status_code = status_code
        self.description = description

    def __str__(self):
        return "HTTP {0}: {1}".format(self.status_code, self.description or http_responses[self.status_code])


class UploadedFile:
    def __init__(self, fileobj, filename, headers=None):
        #: Open file(-like) object (BytesIO buffer or temporary file)
        self.file = fileobj
        filename = normalize('NFC', filename)
        filename = re.split(r'[\\/]', filename)[-1]
        filename = re.sub(r'[^\w. -]', '', filename)
        filename = re.sub(r'[-\s]+', '-', filename).strip('.-/\\')
        self.filename = filename[:255] or 'empty'
        self.headers = headers

    def save(self, dest):
        if isinstance(dest, str):
            with open(dest, 'wb') as dest_fileobj:
                copyfileobj(self.file, dest_fileobj)
        else:
            copyfileobj(self.file, dest)


class HttpRequest(object):
    '''only utf-8 encoding is supported currently
    '''
    MAX_DATA_SIZE = 512 * 1024

    def __init__(self, environ):
        """
        construct the request by the given WSGI environ. it should be safe to
        call, and the parts that may raise exceptions should be done in parse.
        """
        self.environ = environ

        self.scheme = environ["wsgi.url_scheme"]
        self.host = get_host(environ)

        self.method = environ["REQUEST_METHOD"].upper()
        self.version = "HTTP/1.1"

        self.path = (environ.get("SCRIPT_NAME", "") + environ.get("PATH_INFO", "")).encode('latin1').decode('utf8')

        self.query_string = environ.get("QUERY_STRING", "")
        self.path_and_query = self.path + '?' + self.query_string if self.query_string else self.path
        self.url = '{0}://{1}{2}'.format(self.scheme, self.host, self.path_and_query)
        self.base_url = '{0}://{1}{2}'.format(self.scheme, self.host, self.path)

        self.remote_addr = environ.get("REMOTE_ADDR", "")
        self.is_ajax = environ.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        self.query, self.form_data, self.files = [MultiValueDict() for i in range(3)]
        self.data = None

    def parse(self):
        if len(self.url) > 2048:
            raise HttpError(414)

        self.query = MultiValueDict(parse_qs(self.query_string, keep_blank_values=False))

        # Parse request body
        if self.method in ('POST', 'PUT', 'PATCH'):
            content_type = self.environ.get("CONTENT_TYPE", "")
            if content_type.startswith('multipart/'):

                fs_environ = self.environ.copy()
                fs_environ.setdefault('CONTENT_LENGTH', '0')
                fs_environ['QUERY_STRING'] = ''

                fs = cgi.FieldStorage(fp=self.environ['wsgi.input'],
                                      environ=fs_environ,
                                      keep_blank_values=True,
                                      encoding='utf-8')
                self.environ['_cgi.FieldStorage'] = fs  # http://bugs.python.org/issue18394

                for item in fs.list or []:
                    if item.filename:  # item is also of FieldStorage type
                        f = UploadedFile(item.file, item.filename, item.headers)
                        self.files.append(item.name, f)
                        self.form_data.append(item.name, f)

                    else:
                        self.form_data.append(item.name, item.value)
            else:
                content_length = int(self.environ.get('CONTENT_LENGTH', 0))
                if content_length > self.MAX_DATA_SIZE:
                    raise HttpError(413)

                if content_length > 0:
                    body = self.environ['wsgi.input'].read(content_length)
                else:
                    body = b''

                self.body = body

                if content_type.startswith("application/x-www-form-urlencoded"):
                    self.form_data = MultiValueDict(parse_qs(body.decode('utf-8')))
                elif content_type.startswith('application/json'):
                    self.data = json.loads(body.decode('utf-8') or 'null', parse_float=Decimal)

    @property
    def cookies(self):
        """A dictionary of Cookie.Morsel objects."""
        if not hasattr(self, "_cookies"):
            self._cookies = http.cookies.SimpleCookie()
            try:
                self._cookies.load(self.environ.get('HTTP_COOKIE', ''))
            except Exception:
                pass
        return self._cookies

    def get_cookie(self, name, default=None):
        """Gets the value of the cookie with the given name, else default."""
        cookie = self.cookies.get(name)
        return cookie.value if cookie else default

    def close(self):
        for key, uploaded_files in self.files.lists():
            for f in uploaded_files:
                try:
                    f.file.close()
                except OSError:
                    pass


def json_default_handler(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, Enum):
        return obj.name
    raise TypeError('Object of type %s is not JSON serializable.' % type(obj))


def json_encode(obj, default_handler=None):
    return json.dumps(obj, ensure_ascii=False, default=default_handler or json_default_handler)


class HttpResponse:
    def __init__(self, body=b'', status_code=200, content_type=None):
        self.headers = Headers([])
        self.cookies = http.cookies.SimpleCookie()

        self.reset(status_code=status_code, body=body, content_type=content_type)

    def __str__(self):
        return str(self.headers)

    def set_cookie(self, name, value, max_age=None, path="/", domain=None, secure=False, httponly=False):
        cookies = self.cookies
        cookies[name] = value
        if domain is not None:
            cookies[name]["domain"] = domain
        if max_age is not None:
            # IE6,7,8 does not support max-age, all browsers support expires
            cookies[name]["expires"] = max_age
        if path is not None:
            cookies[name]["path"] = path
        if secure:
            cookies[name]['secure'] = True
        if httponly:
            cookies[name]['httponly'] = True

    def delete_cookie(self, name, path="/", domain=None):
        self.set_cookie(name, value="", path=path, max_age=-300000000, domain=domain)

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, s):
        '''
        @param s: a bytes, bytearray, str or any iterable object.
        '''
        if isinstance(s, str):
            s = s.encode('utf-8')
        self._body = s

    def reset(self, body=b'', status_code=200, content_type=None):
        self.status_code = status_code
        self.body = body

        # http://www.w3.org/International/O-HTTP-charset
        # Documents transmitted with HTTP that are of type text, such as
        # text/html, text/plain, etc., can send a charset parameter in the HTTP
        # header to specify the character encoding of the document.

        self.headers['Content-Type'] = content_type or 'text/html; charset=utf-8'

    def __iter__(self):
        if isinstance(self._body, (bytes, bytearray)):
            return iter([self._body])
        # then body must be iterable
        return iter(self._body)

    def close(self):
        if hasattr(self._body, 'close'):
            self._body.close()

    def json(self, obj, default_handler=None):
        self.headers['Content-Type'] = 'application/json'
        self.body = json_encode(obj, default_handler)

    def redirect(self, url, permanent=False):
        self.body = b''
        self.status_code = 301 if permanent else 302
        self.headers['Location'] = url


def inspect(fn):
    if fn.__code__.co_kwonlyargcount > 0:
        raise NotImplementedError('keyword-only args are not supported.')
    # varargs, kwargs can be silently ignored.

    # co_varnames includes local var names besides args.
    # varargs, kwargs, kwonlyargs are not counted in co_argcount.
    args = fn.__code__.co_varnames[:fn.__code__.co_argcount]
    # the args with defaults are in the end
    # when there's no defaults, fn.__defaults__ is None.
    defaults = dict(zip(reversed(args), reversed(fn.__defaults__ or ())))
    return args, defaults, fn.__annotations__


class Controller:
    def __init__(self, app, request, response, route_data, ns, action):
        self.app = app
        self.request = request
        self.response = response
        self.route_data = route_data
        self.ns = ns
        self.action = action

    def redirect_to_url(self, url, *, permanent=False):
        self.response.redirect(url, permanent)

    def redirect_to(self, route_name=None, *, permanent=False, **kwargs):
        url = self.reverse_url(route_name, **kwargs)
        self.response.redirect(url, permanent)

    def render(self, view=None, **kwargs):
        self.response.body = self.render_to_string(view, **kwargs)

    def render_to_string(self, view=None, **kwargs):
        args = self.get_view_context()
        args.update(kwargs)

        path = self.locate_view(view or self.action)
        view = self.app.load_view(self.ns, path)
        return view(**args)

    def locate_view(self, view_name):
        return self.app.locate_view(self, view_name)

    def get_view_context(self):
        return self.app.get_view_context(self)

    def reverse_url(self, name, **kwargs):
        return self.app.reverse_url(name, **kwargs)

    def process(self):
        method = getattr(self, self.action, None)
        if method is None:
            logger.debug("{}: {}.{}@{} does not exist.".format(self.request.path, self.__module__, type(self).__name__, self.action))
            raise HttpError(404)

        # if values in POST were overriden by values got from query string,
        # a fishing attack could be easily done by publishing tampered links.
        request = self.request
        params = request.query.copy()
        params.update(request.form_data)

        params.update(self.route_data)

        args = self._get_method_arguments(method, params)
        method(**args)

    def _get_method_arguments(self, method, params):
        while hasattr(method, '__wrapped__'):
            method = method.__wrapped__

        args, values, annotations = inspect(method)

        def convert(type_, value):
            return type_[value] if issubclass(type_, Enum) else type_(value)

        for name in args[1:]:
            query_values = params.getlist(name)
            type_ = annotations.get(name)
            if type_ is not None:
                assert not isinstance(type_, (tuple, dict)), 'Only primitive types and [] are supported.'
                try:
                    if isinstance(type_, list):
                        type_ = type_[0] if type_ else lambda x: x
                        values[name] = tuple(convert(type_, value) for value in query_values)
                    elif query_values:
                        values[name] = convert(type_, query_values[-1])
                except Exception as e:
                    logger.debug(
                        '{}: Argument type conversion error ({0}.{1}#{2}): {3}\n  {4}'.format(
                            self.request.path, type(self).__module__, type(self).__name__, method.__name__, query_values, e
                        ))
                    raise HttpError(404) from None
            elif query_values:
                values[name] = query_values[-1]  # value default to str type

        if len(args) - 1 != len(values):
            logger.debug(
                '{}: ``{}.{}`` Unexpected parameters ``{}`` received. Should be ``{}``.'.format(
                    self.request.path, type(self).__module__, type(self).__name__, args, tuple(values.keys())
                ))
            raise HttpError(404)
        return values


class Route:
    """Inspired by tornado URLSpec."""

    def __init__(self, methods, pattern, middlewares, uses, name=None):
        """Parameters:

        * ``methods``: an example is ['GET', 'POST']

        * ``pattern``: Regular expression to be matched.  Any groups
          in the regex will be passed in to the controller.

        * ``middlewares``: middleware names

        * ``uses``: controller@action

        * ``name`` (optional): A name for this route.  Used by `reverse`.
        """
        if isinstance(methods, str):
            methods = (methods,)
        self.methods = [method.upper() for method in methods]

        pattern = '^' + pattern + '$'
        self.regex = re.compile(pattern)
        assert len(self.regex.groupindex) == self.regex.groups, \
            ("groups in url regexes must be all named: %r" % self.regex.pattern)

        middlewares = middlewares or tuple()
        self.middlewares = (middlewares,) if isinstance(middlewares, str) else tuple(middlewares)

        self.controller, self.action = uses.split('@')
        self.name = name
        self._path = self._find_groups()
        self._group_names = tuple(self.regex.groupindex.keys())

    def __repr__(self):
        return '%s(%s, %r, name=%r)' % (
            self.__class__.__name__,
            self.methods, self.regex.pattern, self.name)

    def _find_groups(self):
        """Returns a string for reversing a url.

        For example: Given the url pattern /(?P<id>[0-9]{4})/(?P<edit>[a-z-]+)/, this method
        would return '/{id}/{edit}/'
        """
        pattern = self.regex.pattern
        if pattern.startswith('^'):
            pattern = pattern[1:]
        if pattern.endswith('$'):
            pattern = pattern[:-1]

        pieces = []
        in_group = False

        for bit in re.split(r'\(\?P<(\w+)>[^()]+\)', pattern):
            pieces.append('{' + bit + '}' if in_group else bit)
            in_group = not in_group

        # the number of strings that re.split returns is (1 + `number of capture groups`) * `number of matches` + 1
        # in this case, there's 1 capture group, so len(pieces) == 2 * `number of matches` + 1
        if len(pieces) // 2 != self.regex.groups:
            # The pattern is too complicated for our simplistic matching,
            # so we can't support reversing it.
            return None

        return ''.join(pieces)

    def reverse(self, kwargs):
        assert self._path is not None, "Cannot reverse url regex " + self.regex.pattern

        if self._group_names:
            path_args = {}
            for key in self._group_names:
                try:
                    value = kwargs.pop(key)
                except KeyError:
                    raise ValueError('`%s` is required in url reversing %r.' % (key, self.name)) from None
                path_args[key] = quote(str(value))
            path = self._path.format(**path_args)
        else:
            path = self._path

        if kwargs:
            path += '?' + urlencode(kwargs)
        return path


class Router:
    def __init__(self, prefix=''):
        self.routes = []
        self.named_routes = {}
        self.prefix = prefix

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        self._prefix = prefix.strip('/')

    def add_prefix(self, path):
        path = path.strip('/')
        path = self._prefix + '/' + path if path else self._prefix
        return path if path.startswith('/') else '/' + path

    def route(self, methods, pattern, middlewares, uses, name=None):
        route = Route(methods, self.add_prefix(pattern), middlewares, uses, name=name)
        self.routes.append(route)
        if name:
            self.named_routes[name] = route

    def get(self, pattern, middlewares, uses, name=None):
        self.route(['GET'], pattern, middlewares, uses, name)

    def post(self, pattern, middlewares, uses, name=None):
        self.route(['POST'], pattern, middlewares, uses, name)

    def put(self, pattern, middlewares, uses, name=None):
        self.route(['PUT'], pattern, middlewares, uses, name)

    def patch(self, pattern, middlewares, uses, name=None):
        self.route(['PATCH'], pattern, middlewares, uses, name)

    def delete(self, pattern, middlewares, uses, name):
        self.route(['DELETE'], pattern, middlewares, uses, name)

    def resolve(self, method, path):
        for route in self.routes:
            if method in route.methods:
                m = route.regex.match(path)
                if m is not None:
                    return route, m.groupdict()
        return None, None

    def reverse(self, name, **kwargs):
        try:
            route = self.named_routes[name]
        except KeyError:
            raise ValueError('no route named `%s`.' % name)
        return route.reverse(kwargs)


class Application:
    def __init__(self, router, middlewares=None, controllers=None, local_path=None):
        self.router = router
        self.middlewares = middlewares or {}
        self.controllers = controllers or {}
        if local_path:
            self.local_path = local_path
        else:
            assert type(self) != Application, 'Application must be subclassed in your app when local_path is not provided.'
            self.local_path = os.path.dirname(sys.modules[type(self).__module__].__file__)

    def reverse_url(self, name, **kwargs):
        return self.router.reverse(name, **kwargs)

    def before_request(self, request):
        pass

    def after_request(self, request, response):
        pass

    def load_view(self, ns, path):
        raise NotImplementedError('load_view must be implemented if view is used.')

    def locate_view(self, controller, view_name):
        return os.path.join(type(controller).__name__[:-10].lower(), view_name + '.html')

    def get_view_context(self, controller):
        return dict(
            controller=controller,
            request=controller.request,
            reverse_url=controller.reverse_url,
        )

    def __call__(self, environ, start_response):
        request = HttpRequest(environ)
        response = HttpResponse()
        try:
            try:
                self.before_request(request)

                request.parse()

                route, route_data = self.router.resolve(request.method, request.path)
                if route is None:
                    logger.debug('{}: No matching route'.format(request.path))
                    raise HttpError(404)

                try:
                    controller_class = self.controllers[route.controller]
                except KeyError:
                    logger.debug('{}: Controller `{}` not found.'.format(request.path, route.controller))
                    raise HttpError(404)

                if route.action.startswith('_'):
                    logger.debug('{}: Action `{}` shall not start with `_`.'.format(request.path, route.action))
                    raise HttpError(403)

                controller = controller_class(
                    self, request, response, route_data,
                    route.controller.rpartition('.')[0],
                    route.action)
                middlewares = [self.middlewares[mw] for mw in route.middlewares]
                middlewares.reverse()

                action = controller.process
                for mw in middlewares:
                    action = partial(mw, controller=controller, next=action)
                action()

            except HttpError as e:
                response.reset(
                    status_code=e.status_code,
                    body=e.description or http_responses[e.status_code],
                    content_type='text/plain; charset=utf8')
            except Exception as e:
                logger.error(
                    'Internal Server Error (%s): %s',
                    request.remote_addr,
                    request.path,
                    exc_info=e)
                response.reset(
                    status_code=500,
                    body=http_responses[500],
                    content_type='text/plain; charset=utf8')
            finally:
                self.after_request(request=request, response=response)

            self.fix_response(request, response)

            status_text = http_responses[response.status_code]

            status = str(response.status_code) + ' ' + status_text
            headers = [(k, v) for k, v in response.headers.items()]
            for cookie in response.cookies.values():
                headers.append(("Set-Cookie", cookie.OutputString()))
        except Exception:
            # should not happen, just log it and return error.
            logger.exception('Programming error')
            status, headers, response = '500 Internal Server Error', [], [b'Server Error\n']
        finally:
            request.close()  # close uploaded files if used.

        start_response(status, headers)
        return response

    def fix_response(self, request, response):
        """
        Removes the body of responses for HEAD requests, 1xx, 204 and 304
        responses. Ensures compliance with RFC 2616, section 4.3.
        """
        status_code = response.status_code
        if request.method == 'HEAD':
            response.body = b''
        elif status_code == 304 or status_code == 204 or 100 <= status_code < 200:
            response.body = b''

            del response.headers['Content-Length']
            if status_code == 304:
                del response.headers['Content-Type']
        else:
            if isinstance(response.body, (bytes, bytearray)):
                response.headers['Content-Length'] = str(len(response.body))


ETAG_MATCH = re.compile(r'(?:W/)?"((?:\\.|[^"])*)"')


# copied from django
def parse_etags(etag_str):
    """
    Parses a string with one or several etags passed in If-None-Match and
    If-Match headers by the rules in RFC 2616. Returns a list of etags
    without surrounding double quotes (") and unescaped from \<CHAR>.
    """
    etags = ETAG_MATCH.findall(etag_str)
    if not etags:
        # etag_str has wrong format, treat it as an opaque string then
        return [etag_str]
    etags = [e.encode('ascii').decode('unicode_escape') for e in etags]
    return etags


def static_file(request, response, root, path, mimetype='auto', max_age=None, charset='UTF-8'):
    path = posixpath.normpath(path).lstrip('/')
    if path.endswith('/') or path == '':
        raise HttpError(404, 'Directory indexes are not allowed.')

    root = os.path.abspath(root)
    path = os.path.normpath(os.path.join(root, path))

    if not path.startswith(root + os.sep):
        raise HttpError(403)
    if not os.path.exists(path) or not os.path.isfile(path):
        raise HttpError(404)
    if os.path.basename(path).startswith('.') or not os.access(path, os.R_OK):
        raise HttpError(403)

    headers = response.headers

    if mimetype == 'auto':
        mimetype, encoding = mimetypes.guess_type(path)
        if encoding:
            headers['Content-Encoding'] = encoding

    if mimetype:
        if (mimetype[:5] == 'text/' or mimetype in ['application/javascript', 'application/json']) and charset and 'charset' not in mimetype:
            mimetype += '; charset=%s' % charset
        headers['Content-Type'] = mimetype

    stats = os.stat(path)
    headers['Content-Length'] = str(stats.st_size)

    if max_age is not None:
        headers["Cache-Control"] = "max-age=" + str(max_age)

    etag = '{0}-{1}'.format(stats.st_mtime, stats.st_size)

    inm = request.environ.get('HTTP_IF_NONE_MATCH')
    if inm and any(t == etag for t in parse_etags(inm)):
        response.status_code = 304
    else:
        headers['ETag'] = '"' + etag + '"'
        response.body = request.environ.get('wsgi.file_wrapper', FileWrapper)(open(path, "rb"))


class FileWrapper:
    def __init__(self, filelike, buffer_size=2**16):
        self.filelike = filelike
        self.buffer_size = buffer_size
        if hasattr(filelike, 'close'):
            self.close = filelike.close

    def __iter__(self):
        return self

    def __next__(self):
        data = self.filelike.read(self.buffer_size)
        if data:
            return data
        raise StopIteration()


def load_controllers(app_name, ns=None):
    '''
    loads all controllers located in {app_name}.controllers directory.
    if ns is not None or empty string, controllers will be looked up in
    {app_name}.{ns}.controllers directory.

    Every controller class must end with 'Controller'.

    This function returns a dict which keys are controller class names without
    the trailing 'Controller' part, and values are the controller classes.
    '''
    import importlib
    import pkgutil

    pkg_name = '.'.join(filter(None, [app_name, ns, 'controllers']))

    result = {}

    pkg = importlib.import_module(pkg_name)  # ensure pkg has been loaded before subpackages are loaded.
    paths = pkg.__path__

    def onerror(pkg_name):
        logger.warning('loading `%s` failed.', pkg_name)

    for loader, name, is_pkg in pkgutil.walk_packages(paths, pkg_name + '.', onerror):
        module = loader.find_module(name).load_module(name)

        for member_name in dir(module):
            member = getattr(module, member_name)
            if not member_name.startswith('_') and member_name.endswith('Controller')\
                    and member.__module__ == name:  # only load controllers defined in the module.
                result[ns + '.' + member_name[:-10] if ns else member_name[:-10]] = member
    return result


class _Controller(Controller):
    def process(self):
        action = self.route_data.get('action')
        action = action.replace('-', '_') if action else self.action
        try:
            self.render(view=action)
        except FileNotFoundError as e:
            logger.debug(str(e))
            raise HttpError(404) from None


def make_simple_controllers(*names, ns=None):
    return {name if not ns else ns + '.' + name: type(name + 'Controller', (_Controller,), {}) for name in names}
