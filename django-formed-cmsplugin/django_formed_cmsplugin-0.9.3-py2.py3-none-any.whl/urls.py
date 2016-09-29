# coding=utf-8
from django.conf.urls import patterns, url

from cmsplugin_formed_form.views import CMSPluginFormedFormView

urlpatterns = patterns(
    '',
    url(r'^(?P<form_id>[0-9]+)/$', CMSPluginFormedFormView.as_view(), name='cmsplugin_formed_form_action'),
)
