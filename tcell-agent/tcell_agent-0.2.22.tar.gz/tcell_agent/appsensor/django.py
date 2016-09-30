# -*- coding: utf-8 -*-
# Copyright (C) 2015 tCell.io, Inc. - All Rights Reserved

from __future__ import unicode_literals
from __future__ import print_function

from tcell_agent.agent import TCellAgent, PolicyTypes
from tcell_agent.appsensor.manager import app_sensor_manager
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.instrumentation import safe_wrap_function

import json

def django_meta(request):
  meta = AppSensorMeta(
      request._tcell_context.remote_addr ,
      request.META.get("REQUEST_METHOD"),
      request.build_absolute_uri(),
      request._tcell_context.route_id,
      session_id=request._tcell_context.session_id,
      user_id=request._tcell_context.user_id
  )
  return meta

def appsensor_login_failed(request, username):
    appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
    if appsensor_policy is None:
        return
    meta = django_meta(request)
    appsensor_policy.check_login_failure(meta, username)

def django_request_appsensor(request):
    appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
    if appsensor_policy is None:
        return
    meta = django_meta(request)
    request_len = None

    try:
        request_len = int(request.META.get("CONTENT_LENGTH",0))
    except:
        pass

    post_dict = {}
    request_json_body = None

    try:
        if (request_len is not None and request_len > 0):
            post_dict = request.POST
            content_type = request.META.get("CONTENT_TYPE","")
            if content_type.startswith("multipart/form-data") == False:
                # Can't just say post as it may be PUT or maybe something else
                # We're going to make sure some crazy client didn't submit json by mistake
                request_body = request.body
                if (request_len < 2000000 and len(request_body) < 2000000):
                    if content_type.startswith("application/json"):
                        request_json_body = request_body
                    else:
                        if isinstance(request_body, bytes):
                            request_body = request_body.decode('utf-8')
                        if request_body[0] == '{' or request_body[0] == '[':
                            try:
                                json.loads(request_body)
                                post_dict = {}
                                request_json_body = request_body
                            except ValueError as ve:
                                pass
    except Exception as e:
        # Log this?
        pass

    meta.request_data(
        request_len,
        request.GET,
        post_dict,
        request.COOKIES,
        request_json_body,
        request.META.get("HTTP_USER_AGENT"),
        request.FILES
    )
    app_sensor_manager.send_appsensor_data(meta)

def django_response_appsensor(django_response, request, response):
    appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
    if appsensor_policy is None:
        return
    meta = django_meta(request)
    response_content_len = 0
    try:
        if isinstance(response, django_response):
            response_content_len = len(response.content)
    except:
        pass
    response_code = response.status_code
    meta.response_data(response_content_len, response_code)
    app_sensor_manager.send_appsensor_data(meta)

def django_path_parameters_appsensor(request, path_dict):
    appsensor_policy = TCellAgent.get_policy(PolicyTypes.APPSENSOR)
    if appsensor_policy is None:
        return
    meta = django_meta(request)
    meta.path_parameters_data(path_dict)
    app_sensor_manager.send_appsensor_data(meta)
