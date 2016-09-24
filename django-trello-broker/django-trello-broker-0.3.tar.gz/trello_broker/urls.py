from django.conf.urls import url

from .views import BitBucketPostView


urlpatterns = [
    url(r'^$',
        BitBucketPostView.as_view(),
        name='trello_broker_post'),
]
