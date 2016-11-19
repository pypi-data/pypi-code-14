from django.conf.urls import include, url
from . import views
urlpatterns = [
	url(r'^$',views.listShops,name="listShops"),
    url(r'^(?P<shop_id>[\d+])$',views.shopSummary,name="ShopSummary"),
    url(r'^(?P<shop_id>[\d+])/(?P<cycle>[\w]+)$',views.shopSummary,name="ShopSummary"),
    url(r'^(?P<shop_id>[\d+])/(?P<cycle>[\w]+)/(?P<delta>[\d]+)$',views.shopSummary,name="ShopSummary"),
]
