# Copyright 2016 Dustin C. Hatch
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
'''Multi-format response handling

:Created: Jul 1, 2016
:Author: dustin
'''
import milla
import collections
import inspect
import functools


class renders(object):
    '''Mark a method as a renderer for one or more media types

    :param content_types: Internet media types supported by the
       renderer
    '''

    def __init__(self, *content_types):
        self.content_types = content_types

    def __call__(self, func):
        func.renders = self.content_types
        return func


def default_renderer(func):
    '''Mark a :py:class:`VariedResponseMixin` renderer as default'''

    func.default_renderer = True
    return func


class VariedResponseMeta(type):

    def __new__(mcs, name, bases, attrs):
        cls = type.__new__(mcs, name, bases, attrs)
        cls.renderers = {}
        cls.default_type = None
        for attr in attrs.values():
            if not isinstance(attr, collections.Callable):
                continue
            if hasattr(attr, 'renders'):
                for content_type in attr.renders:
                    cls.renderers[content_type] = attr
                if getattr(attr, 'default_renderer', False):
                    cls.default_type = attr.renders[0]
        return cls


_VariedResponseBase = VariedResponseMeta(
    '_VariedResponseBase', (milla.Response,), {})


class VariedResponseBase(_VariedResponseBase):
    '''Base class for responses with variable representations

    In many cases, a a response can be represented in more than one
    format (e.g. HTML, JSON, XML, etc.). This class can be used to
    present the correct format based on the value of the ``Accept``
    header in the request.

    To use this class, create a subclass with a method to render each
    supported representation format. The render methods must have
    a ``renders`` attribute that contains a sequence of Internet media
    (MIME) types the renderer is capable of producing. The
    :py:func:`renders` decorator can be used to set this attribute.

    Each renderer must take at least one argument, which is the context
    data passed to :py:meth:`set_payload`. Additional arguments are
    allowed, but they must be passed through :py:meth:`set_payload` as
    keyword arguments.

    If the ``Accept`` header of the request does not specify a media
    type supported by any renderer, :py:exc:`~webob.exc.NotAcceptable`
    will be raised. To avoid this, select a renderer as the "default"
    by setting its `default_renderer` attribute to ``True`` (e.g. with
    :py:func:`default_renderer`). This renderer will be used for all
    requests unless a more appropriate renderer is available.

    Example:

    .. code-block:: python

        class VariedResponse(Response, VariedResponse):

            @default_renderer
            @renders('text/html')
            def render_html(self, context, template):
                self.body = render_jinja_template(template, context)

            @renders('application/json')
            def render_json(self, context):
                self.body = json.dumps(context)

    The custom response class can be set as the default by extending the
    :py:meth:`~milla.app.BaseApplication.make_request` method. For
    example:

    .. code-block:: python

        class Application(milla.app.Application):

            def make_request(self, environ):
                request = super(Application, self).make_request(environ)
                request.ResponseClass = VariedResponse.for_request(request)
                return request
    '''

    def __init__(self, request, *args, **kwargs):
        super(VariedResponseBase, self).__init__(*args, **kwargs)
        self.request = request

    @classmethod
    def for_request(cls, request):
        return functools.partial(cls, request)

    def set_payload(self, context, **kwargs):
        '''Set the response payload using the most appropriate renderer

        :param context: The data to pass to the renderer
        :param kwargs: Additional keyword arguments to pass to the
           renderer

        This method will determine the most appropriate representation
        format for the response based on the ``Accept`` header in the
        request and delegate to the method that can render that format.

        Example:

        .. code-block:: python

            def controller(request):
                response = VariedResponse.for_request(request)
                response.set_payload(
                    {'hello': 'world'},
                    template='hello.html',
                )
                return response

        In this example, the context is ``{'hello': 'world'}``. This
        will be passed as the first argument to any renderer. If the
        selected renderer accepts a ``template`` argument,
        ``'hello.html'`` will be passed as well.
        '''

        if not self.vary:
            self.vary = ['Accept']
        elif 'accept' not in (v.lower() for v in self.vary):
            self.vary = self.vary + ('Accept',)

        offer_types = self.renderers.keys()
        match = self.request.accept.best_match(offer_types, self.default_type)
        if match is None:
            raise milla.HTTPNotAcceptable
        renderer = self.renderers[match]
        kwargs = _filter_kwargs(renderer, kwargs)
        renderer(self, context, **kwargs)


def _filter_kwargs(func, kwargs):
    if hasattr(inspect, 'signature'):  # Python 3
        sig = inspect.signature(func)
        accepted = (p.name for p in sig.parameters.values()
                    if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD)
    else:  # Python 2
        accepted = inspect.getargspec(func)[0]
    return dict((k, kwargs[k]) for k in accepted if k in kwargs)
