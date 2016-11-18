# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from datetime import date
from django.contrib import auth
from django.conf import  settings
from .models.user_behavior import UserBehavior
from rest_framework.response import Response


def get_request_ip(request):
    if request.META is 'HTTP_X_FORWARDED_FOR':
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


def get_request_data(request):
    server = request.META['HTTP_HOST'].split(':')

    return {
        'client': {
            'ip': get_request_ip(request),
        },
        'server': {
            'host': server[0],
            'port': server[1],
        },
        'request': {
            'method': request.method,
            'path': request.path,
            'data': json.loads(request.body),
        },
    }


def get_response_data(response):
    if isinstance(response, Response):
        return {
            'status_code': response.status_code,
            'data': response.data,
        }
    else:
        return {}


def save_response_data(api_info, response_data):
    api_info.response = response_data
    api_info.save(update_fields=['response'])


def get_es_log_data(request_data, response_data, user):
    request_data['response'] = response_data
    return request_data


def set_es_url():
    hostname = settings.REST_CLIENT_SETTINGS['ES']['default']['HOSTNAME']
    port = settings.REST_CLIENT_SETTINGS['ES']['default']['PORT']
    url = '{}:{}'.format(hostname, port)
    return url


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user


def record(request, obj):
    behavior = UserBehavior(api_info=request.data['api_info'], content_object=obj)
    behavior.save()
