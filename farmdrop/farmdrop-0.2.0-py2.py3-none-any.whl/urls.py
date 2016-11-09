from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve
from oscar.app import application


admin.autodiscover()

urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt', include('robots.urls')),
    url(r'', include(application.urls)),
    #url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
    #    name='django.contrib.sitemaps.views.sitemap'),
]

# This is only needed when using runserver.
if settings.DEBUG:
    import debug_toolbar
    from django.views.static import  serve
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,  # NOQA
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'^__debug__/', include(debug_toolbar.urls))
        ]
