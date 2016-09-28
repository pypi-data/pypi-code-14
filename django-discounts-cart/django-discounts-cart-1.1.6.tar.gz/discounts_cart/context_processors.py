# -*- coding: utf-8 -*-
import re
from decimal import Decimal  # obligatory <<<


def vars_cart(request):

    pattern = re.compile(r'\.[0]+$')
    cart_prod = None
    cart_count = 0
    cart_amount = 0

    if 'cart' in request.session:
        prod_dict = eval(request.session['cart'])
        cart_prod = prod_dict['prod']
        cart_count = prod_dict['count']
        cart_amount = pattern.sub('', str(prod_dict['amount']))
        request.session['cart'] = repr(prod_dict)

    return {
        'cart_prod': cart_prod,
        'cart_count': cart_count,
        'cart_amount': cart_amount
    }
