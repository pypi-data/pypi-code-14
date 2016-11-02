# Copyright 2011 Dustin C. Hatch
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
'''Stub controller classes

These classes can be used as base classes for controllers. While any
callable can technically be a controller, using a class that inherits
from one or more of these classes can make things significantly easier.

:Created: Mar 27, 2011
:Author: dustin
'''

import datetime
import milla.util
import os
try:
    import pkg_resources
except ImportError:
    pkg_resources = None


class Controller(object):
    '''The base controller class

    This class simply provides empty ``__before__`` and ``__after__``
    methods to facilitate cooperative multiple inheritance.
    '''

    def __before__(self, request):
        pass

    def __after__(self, request):
        pass


class FaviconController(Controller):
    '''A controller for the "favicon"

    This controller is specifically suited to serve a site "favicon" or
    bookmark icon. By default, it will serve the *Milla* icon, but you
    can pass an alternate filename to the constructor.

    :param icon: Path to an icon to serve
    :param content_type: Internet media type describing the type of image
       used as the favicon, defaults to 'image/x-icon' (Windows ICO format)
    '''

    #: Number of days in the future to set the cache expiration for the icon
    EXPIRY_DAYS = 365

    def __init__(self, icon=None, content_type='image/x-icon'):
        try:
            if icon:
                self.icon = open(icon, 'rb')
                self.content_type = content_type
            elif pkg_resources:
                self.icon = pkg_resources.resource_stream('milla', 'milla.ico')
                self.content_type = 'image/x-icon'
            else:
                icon = os.path.join(
                    os.path.dirname(milla.__file__),
                    'milla.ico'
                )
                self.icon = open(icon, 'rb')
                self.content_type = 'image/x-icon'
        except (IOError, OSError):
            self.icon = self.content_type = None


    def __call__(self, request):
        if not self.icon:
            raise milla.HTTPNotFound
        response = milla.Response()
        response.app_iter = self.icon
        response.headers['Content-Type'] = self.content_type
        expires = (datetime.datetime.utcnow() +
                   datetime.timedelta(days=self.EXPIRY_DAYS))
        response.headers['Expires'] = milla.util.http_date(expires)
        return response


class HTTPVerbController(Controller):
    '''A controller that delegates requests based on the HTTP method

    Subclasses of this controller should have an instance method for
    every HTTP method they support. For example, to support the ``GET``
    and ``POST`` methods, a class might look like this:

    .. code-block:: python

        class MyController(HTTPVerbController):

            def GET(self, request):
                return 'Hello, world!'

            def POST(self, request):
                return 'Thanks!'
    '''

    def __call__(self, request, *args, **kwargs):
        try:
            func = getattr(self, request.method)
        except AttributeError:
            raise milla.HTTPMethodNotAllowed
        return func(request, *args, **kwargs)

    @property
    def allowed_methods(self):
        for attr in dir(self):
            if attr.upper() == attr:
                yield attr
