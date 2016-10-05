# -*- coding: utf-8 -*-
from rest_framework.exceptions import APIException

class APIError(APIException):
    status_code = 500
    default_detail = 'ALI云 API调用失败'

class ParameterError(APIException):
    status_code = 500
    default_detail = '参数错误'