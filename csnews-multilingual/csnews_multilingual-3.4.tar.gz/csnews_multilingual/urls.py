from django.conf.urls import patterns, url, include
from csnews_multilingual.feeds import LatestNews
# feed_dict = {'rss': LatestNews}


urlpatterns = patterns(
    'csnews_multilingual.views',
    url(r'^$', 'index', name='csnews_index'),
    url(r'^feed/$', LatestNews(), name='csnews_feed'),
    url(r'^archive/', 'archive', name='csnews_archive'),
    url(r'^(?P<article_slug>[\-\d\w]+)/$', 'article_index', name='csnews_article'),
)

urlpatterns += patterns(
    '',
    (r'^photologue/', include('photologue.urls')),
)
