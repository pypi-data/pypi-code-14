# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url
from polybuilder import views

urlpatterns = [
    url(r'^$', views.PolyBuilderView.as_view(), name='polybuilder'),
    url(r'^shared/$', views.SharedComponentsView.as_view(), name='shared'),
]
