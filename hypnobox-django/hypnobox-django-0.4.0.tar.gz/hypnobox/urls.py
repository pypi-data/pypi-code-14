# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex="^lead/create/$",
        view=views.LeadCreateView.as_view(),
        name='new_lead',
    ),
]
