# -*- coding: utf-8 -*-
from __future__ import absolute_import

from functools import wraps
import json
from .serializers import ApiInfoSerializer

from .services import get_request_data, set_response_data

from django.contrib.auth.models import User


def user_behavior_extracter(func):

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        request = args[1]
        request_data = get_request_data(request)

        serializer = ApiInfoSerializer(data=request_data, partial=True)

        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            api_info = serializer.save(user=user)
            request.data['api_info'] = api_info

        queryset = func(*args, **kwargs)
        request.data.pop('api_info')
        set_response_data(api_info, queryset)

        return queryset

    return func_wrapper
