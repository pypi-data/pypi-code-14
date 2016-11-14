# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import (
    RegisterUrlView,
    RedirectShortUrlView,
    ShortUrlMetricsView,
)


app_name = 'shorturls'

urlpatterns = [
    url(
        r'^register/$',
        RegisterUrlView.as_view(),
        name='register_url'
    ),
    url(
        r'^(?P<code>[^/]+)/$',
        RedirectShortUrlView.as_view(),
        name='redirect_url',
    ),
    url(
        r'^metrics/(?P<code>[^/]+)/$',
        ShortUrlMetricsView.as_view(),
        name='shorturl_metrics',
    ),
]
