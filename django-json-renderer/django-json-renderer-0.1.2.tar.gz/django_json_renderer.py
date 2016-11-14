#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
A simple json renderer for django.
'''

__version__ = '0.1.2'
__author__ = 'HakurouKen'
__description__ = 'A Simple json renderer for django.'
__license__ = 'MIT'

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import query, Model
from django.forms.models import model_to_dict

__all__ = ['JsonResponse','ModelJSONEncoder','render_json']

try:
    from functools import wraps
except ImportError:
    def wraps(wrapped, assigned=('__module__', '__name__', '__doc__'),
              updated=('__dict__',)):
        def inner(wrapper):
            for attr in assigned:
                setattr(wrapper, attr, getattr(wrapped, attr))
            for attr in updated:
                getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
            return wrapper
        return inner

try:
    from django.http import JsonResponse
except ImportError:
    from django.http import HttpResponse
    class JsonResponse(HttpResponse):
        ''' Django JsonResponse Class '''
        def __init__(self, data, encoder=DjangoJSONEncoder, safe=True,**kwargs):
            if safe and not isinstance(data, dict):
                raise TypeError(
                    'In order to allow non-dict objects to be serialized set the '
                    'safe parameter to False.'
                )
            if json_dumps_params is None:
                json_dumps_params = {}
            kwargs.setdefault('content_type', 'application/json')
            data = json.dumps(data, cls=encoder)
            super(JsonResponse, self).__init__(content=data)


class ModelJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, query.QuerySet):
            return list(o.values())
        elif isinstance(o, Model):
            return model_to_dict(o)
        else:
            return super(ModelJsonResponse, self).default(o)


def render_json(encoder=ModelJSONEncoder,safe=True,**kwargs):
    '''
        Decorator for Django views that convert serializable object into JsonResponse.

        Parameters:
            Has the same meaning of JsonResponse.
            See ` https://docs.djangoproject.com/en/1.10/ref/request-response/#jsonresponse-objects ` for details.
            For compatibility reasons, `json_dumps_params` is not supported.
    '''
    def renderer(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            ret = func(*args,**kwargs)
            return JsonResponse(ret,encoder,safe,**kwargs)
        return wrapper
    return renderer
