from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<template_id>[0-9a-z\-_]+)/$', views.NavModuleView.as_view())
]
