from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^content-module/(?P<template_id>[0-9a-z\-_]+)/$',
        views.ContentModuleView.as_view()
    ),
    url(
        r'^articles-module/(?P<template_id>[0-9a-z\-_]+)/$',
        views.ArticlesModuleView.as_view()
    )
]
