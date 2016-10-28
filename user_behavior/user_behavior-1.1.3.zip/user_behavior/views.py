# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .filters import ApiInfoFilter, UserBehaviorFilter

from .serializers import ApiInfoSerializer, UserBehaviorSerializer
from .models.api_info import ApiInfo
from .models.user_behavior import UserBehavior


class ApiInfoViewSet(viewsets.ModelViewSet):
    queryset = ApiInfo.objects.all().order_by('id')
    serializer_class = ApiInfoSerializer
    filter_class = ApiInfoFilter

    def list(self, request, *args, **kwargs):
        return super(ApiInfoViewSet, self).list(request)


class UserBehaviorViewSet(viewsets.ModelViewSet):
    queryset = UserBehavior.objects.all()
    serializer_class = UserBehaviorSerializer
    filter_class = UserBehaviorFilter

    def list(self, request, *args, **kwargs):
        api_info_id = request.query_params.get('api_info')
        if api_info_id:
            self.queryset = self.queryset.filter(api_info_id=api_info_id)
        return super(UserBehaviorViewSet, self).list(request)
