from django.conf.urls import url, patterns 

urlpatterns = patterns('django_mce_pygments.views',
    url(r'^renderer/$', 'pygments', name='pygments'),
)
