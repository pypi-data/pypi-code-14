from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.pageView, kwargs={'slug': None, 'homepage': True}),
    url(r'^(?P<slug>[0-9a-z\-_]+)/$', views.pageView),
    url(r'^(?P<path>[0-9a-z\-_/]+)/$', views.contentView)
]
