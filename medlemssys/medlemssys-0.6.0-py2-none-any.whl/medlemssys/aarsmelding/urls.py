from django.conf.urls import patterns, url

urlpatterns = patterns('aarsmelding.views',
    url(r'^$',
        'index', name='aarsmelding_home'),
    url(r'^(?P<lokallag_slug>[-\w]+)/$',
        'single', name='aarsmelding_single'),
)
