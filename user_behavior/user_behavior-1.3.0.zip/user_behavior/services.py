# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import date
from django.conf import  settings
from .models.user_behavior import UserBehavior


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
            'data': request.body,
        },
    }


def set_response_data(api_info, response):
    if type(response).__name__ is 'Response':
        response_data = {
            'status_code': response.status_code,
            'data': response.data,
        }
        api_info.response = response_data
        api_info.save(update_fields=['response'])
    return api_info


def set_es_url():
    hostname = settings.REST_CLIENT_SETTINGS['ES']['default']['HOSTNAME']
    port = settings.REST_CLIENT_SETTINGS['ES']['default']['PORT']
    url = '{}:{}'.format(hostname, port)
    return url


def record(request, obj):
    behavior = UserBehavior(api_info=request.data['api_info'], content_object=obj)
    behavior.save()
