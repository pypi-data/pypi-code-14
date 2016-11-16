# -*- coding:utf-8 -*-
from flask import current_app, request
from flask.views import MethodView

from palmer import exceptions
from palmer.config import default_config


class APIView(MethodView):
    authentication_classes = None
    permission_classes = None
    renderer_class = None

    @property
    def user(self):
        if not hasattr(self, '_user'):
            self.perform_authenticate()
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def platform(self):
        if not hasattr(self, '_platform'):
            self._platform = request.headers.get('X-Platform', None)
        return self._platform

    @property
    def ip_address(self):
        return request.environ.get('REMOTE_ADDR', None)

    @classmethod
    def _get_authentication_classes(cls):
        if cls.authentication_classes is not None:
            return cls.authentication_classes
        if not current_app:
            return default_config.AUTHENTICATION_CLASSES
        return getattr(current_app.api_config, 'AUTHENTICATION_CLASSES',
                       default_config.AUTHENTICATION_CLASSES)

    @classmethod
    def _get_permission_classes(cls):
        if cls.permission_classes is not None:
            return cls.permission_classes
        if not current_app:
            return default_config.PERMISSION_CLASSES
        return getattr(current_app.api_config, 'PERMISSION_CLASSES',
                       default_config.PERMISSION_CLASSES)

    def _get_renderer_class(self):
        if self.renderer_class is not None:
            return self.renderer_class
        if not current_app:
            return default_config.RENDERER_CLASS
        return getattr(current_app.api_config, 'RENDERER_CLASS', default_config.RENDERER_CLASS)

    def get_authenticators(self):
        return [auth() for auth in self._get_authentication_classes()]

    def get_permissions(self):
        return [permission() for permission in self._get_permission_classes()]

    def perform_authenticate(self):
        for authenticator in self.get_authenticators():
            user = authenticator.authenticate()
            if user:
                self.user = user
                return
        self.user = None

    def check_permissions(self):
        """
        Check if the request should be permitted.
        Raises an appropriate exception if the request is not permitted.
        """
        for permission in self.get_permissions():
            if not permission.has_permission(self):
                raise exceptions.PermissionDenied(message=getattr(permission, 'message', None))

    def permission_denied(self, message=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if not self.user:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(message=message)

    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        self.perform_authenticate()
        self.check_permissions()

        pre_process = getattr(self, 'pre_process', None)
        if pre_process is not None:
            pre_process(*args, **kwargs)

        meth_pre_process = getattr(self, '{0}_pre_process'.format(request.method.lower()), None)
        if meth_pre_process is not None:
            meth_pre_process(*args, **kwargs)

        resp = meth(*args, **kwargs)
        request.renderer_class = self._get_renderer_class()
        return resp
