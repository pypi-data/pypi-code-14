from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^code_base_info/$', views.code_base_info, name='code_base_info'),
    
]
