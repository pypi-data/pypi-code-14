from django.conf.urls import patterns, url, include
from report_system import views

urlpatterns = patterns(
    "",
    url(r'^(?P<target_model>[-\w]+)/(?P<id>\d+)/$', views.CreateTicketView.as_view(),
        name="ticket_create_api"),
)