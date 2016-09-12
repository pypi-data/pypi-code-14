from django.conf.urls import url
from ..views import InterviewListView, InterviewDetailView, PreviewInterviewDetailView

urlpatterns = [
    url(r'^$', InterviewListView.as_view(), name='interviews-list'),
    url(r'^preview/(?P<hash>[\w]+)/(?P<slug>[-\w]+)$', PreviewInterviewDetailView.as_view(), name='interviews-preview'),
    url(r'^page-(?P<page>\d+)/$', InterviewListView.as_view(), name='interviews-list-page'),
    url(r'^(?P<filter_key>\w+)-(?P<filter_value>\w+)/$', InterviewListView.as_view(), name='interviews-list-filter'),
    url(r'^(?P<filter_key>\w+)-(?P<filter_value>\w+)/page-(?P<page>\d+)/$', InterviewListView.as_view(), name='interviews-list-filter-page'),
    url(r'^(?P<slug>[-\w]+)$', InterviewDetailView.as_view(), name='interviews-detail'),
]
