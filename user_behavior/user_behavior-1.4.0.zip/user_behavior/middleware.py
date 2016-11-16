# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from django.forms import model_to_dict
from datetime import date

from django.contrib.auth.models import User

from .serializers import ApiInfoSerializer
from .services import get_request_data, set_response_data
from .tasks import task_user_behavior
from django.conf import settings


class UserBehaviorExtractMiddleware(object):

    def __init__(self):
        self._api_info = None

    def __call__(self):
        self._api_info = None

    def process_request(self, request):
        if request.user.id and request.method == 'POST':
            request_data = get_request_data(request)
            self._api_info = request_data

            if hasattr(settings, 'USER_BEHAVIOR_CONFIG') \
                    and settings.USER_BEHAVIOR_CONFIG['LOG_TO_DB']:

                serializer = ApiInfoSerializer(data=request_data, partial=True)

                if serializer.is_valid():
                    user = User.objects.get(id=request.user.id)
                    self._api_info = serializer.save(user=user)

    def process_response(self, request, response):
        if request.method == 'POST':
            api_info = set_response_data(self._api_info, response)
            task_user_behavior(api_info)

        return response
