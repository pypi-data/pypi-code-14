from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^trainer/$',views.UserView.as_view(),name='career'),
	url(r'^trainer/view/(?P<token>[a-zA-Z0-9]+)',views.trainer_view,name='view'),
]
