from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^auth-info/$', views.authInfo),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^activate/$', views.activate),
    url(r'^resend-activation-message/$', views.resend_activation_message),
    url(r'^send-reset-password-message/$', views.send_reset_password_message),
    url(r'^reset-password/$', views.reset_password)
]
