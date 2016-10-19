from django.conf.urls import patterns, include, url
from django_client_logger.views.log_receiver import LogReceiver

urlpatterns = patterns('',
    url(r'log', LogReceiver().run)
)
