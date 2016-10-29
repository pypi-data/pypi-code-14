from django.conf.urls import url
from django_client_logger.views.log_receiver import LogReceiver


urlpatterns = [
    url(r'log', LogReceiver().run)
    ]
