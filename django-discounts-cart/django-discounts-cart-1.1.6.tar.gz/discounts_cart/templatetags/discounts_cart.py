# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()


@register.inclusion_tag('discounts_cart/in_cart_link.html', takes_context=True)
def cart_add_select_product(context, app, model, prod_id, name_in_cart='',
                            name_from_cart='', add_more_name=_('Add more'),
                            flag_img=False):

    action = 'in_cart'
    button_name = name_in_cart
    cart_prod = context['cart_prod']
    class_add_more = 'cart_add_more_product'

    if flag_img:
        class_img = 'cart_img_in'
        cart_img_from = 'cart_img_from'
    else:
        class_img = None
        cart_img_from = None

    if cart_prod is not None and prod_id in cart_prod[app][model]:
        action = 'from_cart'
        button_name = name_from_cart
        class_img = cart_img_from
        class_add_more = 'cart_add_more_product_active'

    return {
        'href': '/cart/add_in_cart/{0}/{1}/{2}/'.format(app, model, prod_id),
        'href_2': '/cart/add_more_product_in_cart/{0}/{1}/{2}/'.format(app, model, prod_id),
        'action': action,
        'button_name': button_name,
        'name_in_cart': name_in_cart,
        'name_from_cart': name_from_cart,
        'class_img': class_img,
        'add_more_name': add_more_name,
        'class_add_more': class_add_more
    }
