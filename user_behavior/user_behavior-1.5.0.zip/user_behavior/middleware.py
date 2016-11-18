# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.models import User
from django.conf import settings
from django.utils.functional import SimpleLazyObject
from importlib import import_module

from .serializers import ApiInfoSerializer
from .services import get_request_data, get_es_log_data, get_user, get_response_data, save_response_data
from .tasks import task_user_behavior


class UserBehaviorExtractMiddleware(object):

    def __init__(self):
        self.engine = import_module(settings.SESSION_ENGINE)

    def __call__(self):
        self.api_info = None

    def set_session(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.engine.SessionStore(session_key)
        request.user = SimpleLazyObject(lambda: get_user(request))

    def method_is_valid(self, request):
        return request.method in settings.USER_BEHAVIOR_CONFIG['METHODS']

    def url_is_valid(self, request):
        return request.path in settings.USER_BEHAVIOR_CONFIG['PERMITTED_URLS']

    def user_is_valid(self, request):
        return hasattr(request, 'user') and request.user.id

    def config_is_valid(self):
        return hasattr(settings, 'USER_BEHAVIOR_CONFIG')

    def is_log_to_db(self):
        return settings.USER_BEHAVIOR_CONFIG['LOG_TO_DB']

    def is_log_to_es(self):
        return settings.USER_BEHAVIOR_CONFIG['LOG_TO_ES']

    def save_request_data(self, request):
        serializer = ApiInfoSerializer(data=self.request_data, partial=True)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            return serializer.save(user=user)

    def process_request(self, request):
        self.set_session(request)

        if self.method_is_valid(request) and self.url_is_valid(request) and self.user_is_valid(request):
            request_data = get_request_data(request)
            self.request_data = request_data

            if self.config_is_valid() and self.is_log_to_db():
                self.api_info = self.save_request_data(request)

    def process_response(self, request, response):
        if self.method_is_valid(request) and self.url_is_valid(request) and self.user_is_valid(request):
            response_data = get_response_data(response)

            if self.config_is_valid() and self.is_log_to_db():
                save_response_data(self.api_info, response_data)

            if self.config_is_valid() and self.is_log_to_es():
                es_log_data = get_es_log_data(self.request_data, response_data, request.user)
                task_user_behavior(es_log_data)

        return response
