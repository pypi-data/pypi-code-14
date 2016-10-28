# -*- coding: utf-8 -*-
import django_filters
from django_filters.filters import MethodFilter

from django.contrib.auth.models import User
from .models.api_info import ApiInfo
from .models.user_behavior import UserBehavior


class ApiInfoFilter(django_filters.FilterSet):
    user = MethodFilter(action='user_filter')
    status_code = MethodFilter(action='status_code_filter')

    class Meta:
        model = ApiInfo
        fields = ('user', 'status_code')

    @classmethod
    def user_filter(cls, queryset, username):
        return queryset.filter(user__username__contains=username)

    @classmethod
    def status_code_filter(cls, queryset, status_code):
        id_list = []
        for qs in queryset:
            if qs.response.has_key('status_code'):
                if qs.response['status_code'] is int(status_code):
                    id_list.append(qs.id)
        return queryset.filter(id__in=id_list)


class UserBehaviorFilter(django_filters.FilterSet):
    model = MethodFilter(action='model_filter')
    api_info = MethodFilter(action='api_info_filter')

    class Meta:
        model = UserBehavior
        fields = ('model', )

    @classmethod
    def model_filter(cls, queryset, name):
        id_list = []
        for qs in queryset:
            if qs.content_type.model == name:
                id_list.append(qs.id)
        return queryset.filter(id__in=id_list)

    @classmethod
    def api_info_filter(cls, queryset, api_info):
        return queryset.filter(api_info__id=api_info)
