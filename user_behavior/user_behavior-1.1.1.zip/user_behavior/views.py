# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .serializers import ApiInfoSerializer

from .models.api_info import ApiInfo


class UserBehaviorViewSet(viewsets.ModelViewSet):
    queryset = ApiInfo.objects.all()
    serializer_class = ApiInfoSerializer
