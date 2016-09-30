from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser

from rest_framework.request import Request
from rest_framework.settings import api_settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object

import copy

import logging

logger = logging.getLogger('auth_anywhere.middleware')

def get_drf_user(request, initial_user):
    """
    This middleware attempts to authenticate requests using DRF middleware.

    Returns: instance of user object or the original value of suer
    """
    user = initial_user

    try:
        authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
        authenticators = [authenticator() for authenticator in authentication_classes]

        # Prevent recursion by setting the User to none for the request which authenticators inspect
        new_request = copy.copy(request)
        new_request.user = None
        drf_request = Request(new_request)

        for authenticator in authenticators:
            user_auth_tuple = authenticator.authenticate(drf_request)

            if user_auth_tuple is not None:
                user = user_auth_tuple[0]

    except Exception as e:
        logging.error(e)
        raise e

    return user

class AuthenticationMiddleware(MiddlewareMixin):

    def _add_lazy_user(self, request):
        """
        Adds a lazy user value to request which is filled in by get_drf_user
        """
        initial_user = request.user
        request.user = SimpleLazyObject(lambda : get_drf_user(request, initial_user))

    def process_request(self, request):
        self._add_lazy_user(request)
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        self._add_lazy_user(request)
        return None
