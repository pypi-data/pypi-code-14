from django.conf.urls import url
from . import views

app_name = 'analysis'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sql/$', views.sql_index, name='sql_index'),
    url(r'^sql/(?P<request_id>[0-9]+)/$', views.sql_detail, name='sql_detail'),
    url(r'^sql/clean/$', views.sql_clean, name='sql_clean')
]
