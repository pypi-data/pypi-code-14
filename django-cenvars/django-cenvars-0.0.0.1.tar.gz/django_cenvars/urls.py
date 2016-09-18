"""
URLs
"""
from django.conf.urls import url
from . import views

# pylint: disable=invalid-name
urlpatterns = [\
    url(r'^cenvars/(?P<identifier>[0-9a-fA-F]{56})/$', views.view),
]
