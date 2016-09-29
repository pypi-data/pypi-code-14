# coding=utf-8
from django.conf.urls import patterns, url

from views import FormDefinitionView

urlpatterns = patterns(
    '',
    url(r'^(?P<pk>[0-9]+)/$', FormDefinitionView.as_view()),
)
