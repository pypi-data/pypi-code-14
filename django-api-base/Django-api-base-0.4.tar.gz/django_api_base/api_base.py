from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings
from .models import UserProfile
import json


class StatusCode(View):
    # Success Codes
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_202_ACCEPTED = 202
    HTTP_203_NON_AUTHORITATIVE = 203
    HTTP_204_NO_CONTENT = 204
    HTTP_205_RESET_CONTENT = 205
    HTTP_206_PARTIAL_CONTENT = 206

    # Client Error Codes
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_402_PAYMENT_REQUIRED = 402
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_405_METHOD_NOT_ALLOWED = 405
    HTTP_406_NOT_ACCEPTABLE = 406
    HTTP_408_REQUEST_TIMEOUT = 408
    HTTP_409_CONFLICT = 409
    HTTP_410_GONE = 410
    HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
    HTTP_426_FORCE_UPDATE = 426

    # Server Error Codes
    HTTP_500_INTERNAL_SERVER_ERROR = 500
    HTTP_501_NOT_IMPLEMENTED = 501
    HTTP_502_BAD_GATEWAY = 502
    HTTP_503_SERVICE_UNAVAILABLE = 503
    HTTP_504_GATEWAY_TIMEOUT = 504


# REST Api parent class. This class is extended to perform the common functionality of a REST api
class ApiView(View):
    flag = StatusCode.HTTP_403_FORBIDDEN
    NULL_VALUE_VALIDATE = [None, '', ' ']

    def get(self, request):
        dic = {'message': "GET Method is not allowed"}
        return JsonWrapper(dic, StatusCode.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        dic = {'message': "POST Method is not allowed"}
        return JsonWrapper(dic, StatusCode.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request):
        dic = {'message': "PUT Method is not allowed"}
        return JsonWrapper(dic, StatusCode.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request):
        dic = {'message': "DELETE Method is not allowed"}
        return JsonWrapper(dic, StatusCode.HTTP_405_METHOD_NOT_ALLOWED)


# This class is for wrapping the json response
class JsonWrapper(JsonResponse):
    def __init__(self, data, flag):
        wrapper_dic = {
            'status': flag,
            'data': data
        }
        super(JsonWrapper, self).__init__(wrapper_dic, status=flag, json_dumps_params={"indent": 4})


# Decorator for getting data from raw body data
def get_raw_data(func):
    def get_data(request, *args, **kwargs):
        json_data = request.body

        try:
            kwargs['data'] = json.loads(json_data)

        except:
            dic = {'message': "Please provide json data and GET Method is not allowed"}
            flag = StatusCode.HTTP_400_BAD_REQUEST
            return JsonWrapper(dic, flag)

        return func(request, *args, **kwargs)

    return get_data


# Decorator for getting the access token
def verify_access_token(func):
    def verify(request, *args, **kwargs):
        flag = StatusCode.HTTP_400_BAD_REQUEST
        access_token = request.META.get('HTTP_ACCESS_TOKEN')
        device_id = request.META.get('HTTP_DEVICE_ID')
        if access_token is not None:
            try:
                if settings.API_TESTING:
                    user_profile_obj = UserProfile.objects.get(access_token=access_token)
                    if user_profile_obj.verify_access_token_expiry():
                        kwargs['user'] = user_profile_obj
                    else:
                        raise UserProfile.DoesNotExist

                else:
                    if device_id is not None:
                        user_profile_obj = UserProfile.objects.get(
                            device_id__device_id=device_id, access_token=access_token)
                        if user_profile_obj.verify_access_token_expiry():
                            kwargs['user'] = user_profile_obj
                        else:
                            raise UserProfile.DoesNotExist
                    else:
                        dic = {"message": "PLEASE PROVIDE A DEVICE ID"}
                        return JsonWrapper(dic, flag)

            except UserProfile.DoesNotExist:
                dic = {"message": "SESSION EXPIRED"}
                flag = StatusCode.HTTP_401_UNAUTHORIZED
                return JsonWrapper(dic, flag)

        else:
            dic = {"message": "PLEASE PROVIDE AN ACCESS TOKEN"}
            return JsonWrapper(dic, flag)

        return func(request, *args, **kwargs)

    return verify
