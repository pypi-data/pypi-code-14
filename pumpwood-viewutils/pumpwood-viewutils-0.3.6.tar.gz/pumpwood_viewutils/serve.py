#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def serve_X_Accel_protected(request, **kwargs):
    '''
        Verify if user is logged and serve files in Ngnix using X-Accel to avoid django overhead
    '''
    print 'request.path: ', request.path
    response = HttpResponse()
    response['X-Accel-Redirect'] = request.path
    return response

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def serve_X_Accel_unprotected(request, **kwargs):
    '''
        Serve files in Ngnix using X-Accel to avoid django overhead
    '''
    print 'request.path: ', request.path
    response = HttpResponse()
    response['X-Accel-Redirect'] = request.path
    print response
