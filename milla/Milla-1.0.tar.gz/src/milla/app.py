# Copyright 2011, 2012, 2014-2016 Dustin C. Hatch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''Module milla.app

The :py:class:`BaseApplication` class is the core of the Milla
framework. This class implements a WSGI application that dispatches
requests to callables based on their URL-path.

Most applications can use :py:class:`Application` directly, without
creating a sub-class. For advanced use, applications can define a
sub-class of :py:class:`BaseApplication` and customize the behavior of
the framework.

:Created: Mar 26, 2011
:Author: dustin
'''

from milla import util
from milla.controllers import FaviconController
from webob.exc import HTTPNotFound, WSGIHTTPException, HTTPMethodNotAllowed
import milla.dispatch.traversal
import os
import sys


__all__ = [
    'Application',
    'BaseApplication',
]


try:
    # In Python 2, it could be a str or a unicode object
    _string = basestring
except NameError:
    # In Python 3, we are only interested in str objects
    _string = str


class BaseApplication(object):
    '''Base class for Milla applications

    This class can be used by applications that need to customize the
    behavior of the framework. In most cases, :py:class:`Application`
    instances can be created directly and a sublcass is not necessary.
    '''

    DEFAULT_CONFIG = {}

    #: Enable HTTP method emulation for POST requests?
    post_method_emulation = True

    def __init__(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self.dispatcher = None

    def __call__(self, environ, start_response):
        start_response = StartResponseWrapper(start_response)
        func = self.resolve_path(environ['PATH_INFO'])
        request = self.make_request(environ)
        request.__dict__['start_response'] = start_response

        try:
            allowed_methods = self._find_attr(func, 'allowed_methods')
        except AttributeError:
            allowed_methods = milla.DEFAULT_METHODS
        if request.method == 'HEAD':
            request.real_method = 'HEAD'
            request.method = 'GET'
        else:
            request.real_method = request.method
        if request.method not in allowed_methods:
            allow_header = {'Allow': ', '.join(allowed_methods)}
            if request.method == 'OPTIONS':
                def func(request):
                    response = request.ResponseClass()
                    response.headers = allow_header
                    return response
            else:
                def func(request):
                    raise HTTPMethodNotAllowed(headers=allow_header)

        try:
            self._call_before(func)(request)
            response = func(request)
        except:
            response = self.handle_error(request)
        finally:
            self._call_after(func)(request)

        # The callable might have returned just a string, which is OK,
        # but we need to wrap it in a Response object
        if isinstance(response, _string) or not response:
            response = request.ResponseClass(response)

        return response(environ, start_response)

    def _call_after(self, func):
        try:
            return self._find_attr(func, '__after__')
        except AttributeError:
            return lambda r: None

    def _call_before(self, func):
        try:
            return self._find_attr(func, '__before__')
        except AttributeError:
            return lambda r: None

    def _find_attr(self, obj, attr):
        try:
            # Object has the specified attribute itself
            return getattr(obj, attr)
        except AttributeError:
            # Object is a bound method; look for the attribute on the instance
            if hasattr(obj, '__self__'):
                return self._find_attr(obj.__self__, attr)
            # Object is a partial; look for the attribute on the inner function
            elif hasattr(obj, 'func'):
                return self._find_attr(obj.func, attr)
            raise

    def update_config(self, filename):
        '''Update application configuration from a file

        :param filename: Path to configuration file

        This method will update the application configuration using
        the values found in the specified configuration file. If the
        specified file does not exist or is not accessible, no
        changes will be made.

        The configuration file will be read using
        :py:func:`milla.util.read_config`.
        '''

        if filename and os.access(filename, os.R_OK):
            self.config.update(util.read_config(filename))

    def make_request(self, environ):
        '''Create a :py:class:`~milla.Request` from a WSGI environment

        :param environ: WSGI environment dictionary
        :returns: :py:class:`milla.Request` object for this request
        '''

        request = milla.Request(environ)
        request.__dict__['config'] = self.config.copy()
        # Sometimes, hacky applications will try to "emulate" some HTTP
        # methods like PUT or DELETE by specifying an _method parameter
        # in a POST request.
        if self.post_method_emulation:
            if request.method == 'POST' and '_method' in request.POST:
                request.method = request.POST.pop('_method')
        return request

    def resolve_path(self, path_info):
        '''Find the controller for a given path

        :param path_info: The request path, relative to the application
        :returns: Controller callable

        If no controller could be resolved for the path, a function
        that raises :py:exc:`HTTPNotFound` will be returned.
        '''

        def path_not_found(request):
            raise HTTPNotFound

        path_not_found.allowed_methods = milla.ALL_METHODS

        try:
            return self.dispatcher.resolve(path_info)
        except milla.dispatch.UnresolvedPath:
            if (path_info == '/favicon.ico' and
                    util.asbool(self.config.get('milla.favicon'))):
                return FaviconController()
            else:
                return path_not_found

    def handle_error(self, request):
        '''Handle errors raised by controller callables

        Subclasses can override this method to customize the error
        handling behavior of applications. The default implementation
        only handles :py:exc:`WSGIHTTPException` exceptions, by calling
        them as WSGI applications
        '''

        typ, value, tb = sys.exc_info()
        if issubclass(typ, WSGIHTTPException):
            return value
        raise


class Application(BaseApplication):
    '''Represents a Milla web application

    Constructing an ``Application`` instance needs a dispatcher, or
    alternatively, a root object that will be passed to a new
    :py:class:`milla.dispatch.traversal.Traverser`.

    :param obj: An object implementing the dispatcher protocol, or an
       object to be used as the root for a Traverser

    ``Application`` instances are WSGI applications.

    .. py:attribute:: config

       A mapping of configuration settings. For each request, the
       configuration is copied and assigned to ``request.config``.
    '''

    DEFAULT_CONFIG = {
        'milla.favicon': True,
    }

    def __init__(self, obj):
        super(Application, self).__init__()
        if not hasattr(obj, 'resolve'):
            # Object is not a dispatcher, but the root object for traversal
            obj = milla.dispatch.traversal.Traverser(obj)
        self.dispatcher = obj


class StartResponseWrapper():

    def __init__(self, start_response):
        self.start_response = start_response
        self.called = False

    def __call__(self, *args, **kwargs):
        if not self.called:
            self.called = True
            self.start_response(*args, **kwargs)
