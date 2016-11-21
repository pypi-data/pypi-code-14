from django.conf.urls import url

from rest_framework_jwt import views as jwt_views

from . import views


urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^refresh-token/', jwt_views.refresh_jwt_token),
    url(r'^register/$', views.register),
    url(r'^activate/$', views.activate),
    url(r'^resend-activation-message/$', views.resend_activation_message),
    url(r'^send-reset-password-message/$', views.send_reset_password_message),
    url(r'^reset-password/$', views.reset_password)
]
