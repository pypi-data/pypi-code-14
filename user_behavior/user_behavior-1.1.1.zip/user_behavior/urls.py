# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers

from .views import UserBehaviorViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'user_behavior', UserBehaviorViewSet)

url_patterns = [
    url(r'', include(router.urls)),
]
