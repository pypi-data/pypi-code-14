from django.conf.urls import url
from congo.conf import settings

urlpatterns = [
    # maintenance
    url(r'^reset-server/$', 'congo.maintenance.views.reset_server', name = 'reset_server'),
    url(r'^r/(?P<content_type_id>[\d]+)/(?P<object_id>[\d]+)/$', 'congo.maintenance.views.redirect', name = "redirect"),

    url(r'^admin/clear-cache/$', 'congo.maintenance.admin_views.clear_cache', name = 'clear_cache'),

    # http errors
    url(r'^400/$', 'congo.maintenance.views.http_error', {'error_no': 400}, name = "http_400"),
    url(r'^403/$', 'congo.maintenance.views.http_error', {'error_no': 403}, name = "http_403"),
    url(r'^404/$', 'congo.maintenance.views.http_error', {'error_no': 404}, name = "http_404"),
    url(r'^500/$', 'congo.maintenance.views.http_error', {'error_no': 500}, name = "http_500"),
    url(r'^503/$', 'congo.maintenance.views.http_error', {'error_no': 503}, name = "http_503"),

    # ajax
    url(r'^congo/maintenance/ajax/(?P<action>[\w\-]+)/$', 'congo.maintenance.ajax_views.ajax', name = "maintenance_ajax"),
]

if settings.CONGO_EMAIL_MESSAGE_MODEL:
    # communication
    urlpatterns += [
        url(r'^admin/test-mail/$', 'congo.communication.admin_views.test_mail', name = 'test_mail'),
        url(r'^preview-email/(?P<message_id>[\d]+)/$', 'congo.communication.views.preview_email', name = "email_preview"),
    ]

