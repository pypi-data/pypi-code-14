# -*- coding: utf-8 -*-
from __future__ import absolute_import

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
            'data': request.data,
        },
    }


def set_response_data(api_info, queryset):
    response = {
        'status_code': queryset.status_code,
        'data': queryset.data,
    }
    api_info.response = response
    api_info.save(update_fields=['response'])


def record(api_info, obj):
    behavior = UserBehavior(api_info=api_info, content_object=obj)
    behavior.save()
