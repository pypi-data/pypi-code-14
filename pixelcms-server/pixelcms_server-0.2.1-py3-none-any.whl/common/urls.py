from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve as static_serve

from filebrowser.sites import site

from . import api_urls

urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^api-docs/', include('rest_framework_docs.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls))
]

if settings.DEBUG:
    urlpatterns += [
        url(
            r'^media/(?P<path>.*)$', static_serve,
            {'document_root': settings.MEDIA_ROOT}
        ),
        url(
            r'^static/(?P<path>.*)$', static_serve,
            {'document_root': settings.STATIC_ROOT}
        )
    ]
