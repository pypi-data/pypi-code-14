# -*- coding:utf-8 -*-
import os
import sys
from itertools import chain

import inflection
from flask import Flask, request
from flask._compat import text_type, string_types, reraise
from werkzeug.exceptions import HTTPException

from palmer.compat import is_flask_legacy
from palmer.config import APIConfig
from palmer.exceptions import APIException, NotFound, MethodNotAllowed
from palmer.request import APIRequest
from palmer.response import APIResponse
from palmer.session import ItsdangerousSessionInterface
from palmer.utils import http_statuses


class Palmer(Flask):
    request_class = APIRequest
    response_class = APIResponse

    #: Better Client-side sessions (http://flask.pocoo.org/snippets/51/)
    session_interface = ItsdangerousSessionInterface()

    def __init__(self, *args, **kwargs):
        super(Palmer, self).__init__(*args, **kwargs)
        self.api_config = APIConfig(self.config)

    def init_config(self, pkg, default='base', local='local', env_name='PALMER_ENV'):
        """
        :: Example

        app.config.base.py
        -------
        BaseConfig(object):
            pass

        app.config.stage.py
        --------
        StageConfig(BaseConfig):
            pass

        app.config.__init__.py
        ------

        app = Palmer(__name__)
        app.init_config('app.config')
        """

        env = os.environ.get(env_name, None)
        name = env or default
        try:
            obj = __import__('{0}.{1}'.format(pkg, name), globals(), locals(), ['object'], 0)
            config = getattr(obj, '{0}Config'.format(inflection.camelize(name)))
        except (ImportError, KeyError, TypeError) as e:
            raise e
        self.config.from_object(config)
        self.config['CONFIG_NAME'] = name

        if not env:
            try:
                obj = __import__('{0}.{1}'.format(pkg, local), globals(), locals(), ['object'], 0)
                config = getattr(obj, '{0}Config'.format(inflection.camelize(local)))
            except (ImportError, KeyError) as e:
                pass
            else:
                self.config.from_object(config)
        self.api_config = APIConfig(self.config)

    def init_controllers(self):
        pass

    def make_response(self, rv):
        """
        We override this so that we can additionally handle
        list and dict types by default.
        """
        # super(Palmer, self).make_response()
        status_or_headers = headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))

        if rv is None and status_or_headers:
            raise ValueError('View function did not return a response')

        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        if not isinstance(rv, self.response_class):
            if isinstance(rv, (text_type, bytes, bytearray, list, dict)):
                rv = self.response_class(rv, headers=headers, status=status_or_headers)
                headers = status_or_headers = None
            else:
                rv = self.response_class.force_type(rv, request.environ)

        if status_or_headers is not None:
            if isinstance(status_or_headers, string_types):
                rv.status = status_or_headers
            else:
                rv.status_code = status_or_headers
        if headers:
            rv.headers.extend(headers)
        return rv

    def handle_user_exception(self, e):
        """
        We override the default behavior in order to deal with APIException.
        """
        exc_type, exc_value, tb = sys.exc_info()
        assert exc_value is e

        if isinstance(e, HTTPException) and not self.trap_http_exception(e):
            return self.handle_http_exception(e)

        if isinstance(e, APIException):
            return self.handle_api_exception(e)

        blueprint_handlers = ()
        handlers = self.error_handler_spec.get(request.blueprint)
        if handlers is not None:
            blueprint_handlers = handlers.get(None, ())
        app_handlers = self.error_handler_spec[None].get(None, ())
        if is_flask_legacy():
            for typecheck, handler in chain(blueprint_handlers, app_handlers):
                if isinstance(e, typecheck):
                    return handler(e)
        else:
            for typecheck, handler in chain(dict(blueprint_handlers).items(),
                                            dict(app_handlers).items()):
                if isinstance(e, typecheck):
                    return handler(e)

        debug = self.config.get('DEBUG', False)
        testing = self.config.get('TESTING', False)
        if debug or testing:
            return reraise(exc_type, exc_value, tb)
        return self.handle_api_exception(APIException())

    def handle_http_exception(self, e):
        description = getattr(e, 'description', None)
        status_code = getattr(e, 'code', None)
        exc_cls = APIException
        if status_code == http_statuses.HTTP_404_NOT_FOUND:
            exc_cls = NotFound
        elif status_code == http_statuses.HTTP_405_METHOD_NOT_ALLOWED:
            exc_cls = MethodNotAllowed
        return self.handle_api_exception(exc_cls(message=description, status_code=status_code))

    def handle_api_exception(self, exc):
        return self.response_class(
            dict(message=exc.message, errors=exc.errors, code=exc.__class__.__name__),
            status=exc.status_code,
        )


