from django.conf.urls import url, patterns 

urlpatterns = patterns('django_mce_spellcheck.views',
    url(r'^$', 'spellcheck', name='spellcheck'),
)
