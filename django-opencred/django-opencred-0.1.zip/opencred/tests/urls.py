from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse

from opencred.settings import SETTINGS

urlpatterns = [
    url(r"^/", lambda r: HttpResponse('hello'), name='index'),
    url(r"^admin/", include(admin.site.urls)),
]

if SETTINGS.OPENCRED_AUTH_BACKEND == 'django-user-accounts':
    urlpatterns += [url(r"^account/", include("account.urls")), ]
if SETTINGS.OPENCRED_AUTH_BACKEND == 'allauth':
    urlpatterns += [url(r'^accounts/', include('allauth.urls')), ]
if SETTINGS.OPENCRED_AUTH_BACKEND == 'contrib-auth':
    urlpatterns += [url(r"^auth/", include('django.contrib.auth.urls')), ]
