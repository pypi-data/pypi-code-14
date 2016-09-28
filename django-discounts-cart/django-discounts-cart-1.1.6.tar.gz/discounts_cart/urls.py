# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'discounts_cart.views',
    url(r'^add_in_cart/(?P<app>[-_\w]+)/(?P<model>[-_\w]+)/(?P<pk>[\d]+)/$', 'add_in_cart', name='add_in_cart'),
    url(r'^add_more_product_in_cart/(?P<app>[-_\w]+)/(?P<model>[-_\w]+)/(?P<pk>[\d]+)/$',
        'add_more_product_in_cart', name='add_more_product_in_cart'),
    url(r'^recalculation_cart_with_promo_code/$', 'recalculation_cart_with_promo_code',
        name='recalculation_cart_with_promo_code'),
    url(r'^$', 'view_cart', name='view_cart'),
)
