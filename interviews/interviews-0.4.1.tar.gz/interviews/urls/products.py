from django.conf.urls import url
from ..views import ProductDetailView, ProductListView

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='product-list'),
    url(r'^page-(?P<page>\d+)/$', ProductListView.as_view(), name='product-list-page'),
    url(r'^(?P<slug>[-\w]+)$', ProductDetailView.as_view(), name='product-detail'),
]
