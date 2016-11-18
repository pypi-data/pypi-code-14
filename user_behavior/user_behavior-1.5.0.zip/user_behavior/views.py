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


class UserBehaviorViewSet(viewsets.ModelViewSet):
    queryset = UserBehavior.objects.all()
    serializer_class = UserBehaviorSerializer
    filter_class = UserBehaviorFilter
