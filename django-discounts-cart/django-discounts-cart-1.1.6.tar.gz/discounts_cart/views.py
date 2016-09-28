# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext as _

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
import re
from django.db.models import Q

from models import Discount


def checking_recalculation(prod):
    from utils import get_optimal_price
    amount = Decimal(0)

    for app, models in prod.items():
        for model, prod_id in models.items():
            for pk, count in prod_id.items():
                product_type = ContentType.objects.get(app_label=app, model=model)
                product = product_type.get_object_for_this_type(id=pk)
                amount += Decimal(get_optimal_price(product)) * Decimal(count)
    return Decimal(amount).quantize(Decimal('0.01'))


def check_promo_code_products(prod, promo_code, flag_user_registered):

    from utils import percent_max_promo_code
    flag_discount = False

    for app, models in prod.items():
        if flag_discount:
            break
        for model, prod_id in models.items():
            for pk in prod_id.keys():
                product_type = ContentType.objects.get(app_label=app, model=model)
                product = product_type.get_object_for_this_type(id=pk)
                percent_max = percent_max_promo_code(product, promo_code, flag_user_registered)

                if percent_max:
                    flag_discount = True

    return flag_discount


def get_specific_amount(prod, promo_code, flag_user_registered):

    from utils import func_specific_amount
    amount = Decimal(0)

    for app, models in prod.items():
        for model, prod_id in models.items():
            for pk, count in prod_id.items():
                product_type = ContentType.objects.get(app_label=app, model=model)
                product = product_type.get_object_for_this_type(id=pk)
                amount += func_specific_amount(product, promo_code, flag_user_registered) * Decimal(count)

    return amount


def view_cart(request):

    products = []

    if 'cart' in request.session:
        prod_dict = eval(request.session['cart'])
        prod = prod_dict['prod']

        for app, models in prod.items():
            for model, prod_id in models.items():
                for pk, count in prod_id.items():
                    product_type = ContentType.objects.get(app_label=app, model=model)
                    product = product_type.get_object_for_this_type(id=pk)
                    setattr(product, 'count', count)
                    products.append(product)

    return render(request, 'cart.html', {'products': products})


def add_in_cart(request, app=None, model=None, pk=None):

    if request.is_ajax() and request.method == 'POST':
        action = request.POST['action']
        pk = int(pk)

        if 'cart' in request.session:
            prod_dict = eval(request.session['cart'])
        else:
            prod_dict = {'prod': {}, 'count': 0, 'amount': Decimal(0)}

        if action == 'in_cart':

            prod_dict['prod'].setdefault(app, {model: {}})
            prod_dict['prod'][app][model].setdefault(pk, 0)
            prod_dict['prod'][app][model][pk] += 1
            prod_dict['count'] += 1
            prod_dict['amount'] = checking_recalculation(prod_dict['prod'])
            request.session['cart'] = repr(prod_dict)

        else:
            count_delete = prod_dict['prod'][app][model][pk]
            prod_dict['prod'][app][model].pop(pk)
            prod_dict['count'] -= count_delete
            prod_dict['amount'] = checking_recalculation(prod_dict['prod'])
            request.session['cart'] = repr(prod_dict)

        pattern = re.compile(r'\.[0]+$')

        response = {
            'success': True,
            'count': str(prod_dict['count']),
            'amount': pattern.sub('', str(prod_dict['amount']))
        }
    else:
        response = {'success': False, 'errors': 'error cart'}

    return JsonResponse(response)


def recalculation_cart_with_promo_code(request):

    if request.is_ajax() and request.method == 'POST':

        user = request.user
        count_prod = 0
        decrease = Decimal(0)
        specific_amount = Decimal(0)
        promo_code = request.POST['promo_code'].strip()
        count_char_in_promo_code = len(promo_code)

        if not promo_code:
            response = {'success': False, 'errors': _('Please enter a promo-code')}
            return JsonResponse(response)

        if user.is_authenticated():
            flag_user_registered = True
        else:
            flag_user_registered = False

        if count_char_in_promo_code != 12 or \
                (count_char_in_promo_code == 12 and
                 not Discount.objects.filter(Q(active=True), Q(use_promo_codes=True),
                                             Q(only_registered=False) |
                                             Q(only_registered=flag_user_registered),
                                             Q(promo_codes__contains=promo_code)).count()):

            response = {'success': False, 'errors': _('Your promo-code is not valid')}
            return JsonResponse(response)
        elif Discount.objects.filter(active=True, use_promo_codes=True,
                                     only_registered=True,
                                     promo_codes__contains=promo_code).count():
            response = {'success': False, 'errors': _('Your promo-code is only for registered users')}
            return JsonResponse(response)

        if 'cart' in request.session:
            prod_dict = eval(request.session['cart'])
            prod = prod_dict['prod']
            # For products with a promo code, taken full price
            specific_amount = get_specific_amount(prod, promo_code, flag_user_registered)

            if not check_promo_code_products(prod, promo_code, flag_user_registered):
                response = {'success': False, 'errors': _('Your promo-code does not belong to the selected products')}
                return JsonResponse(response)

            from utils import recalculation_with_promo_code

            for app, models in prod.items():
                for model, prod_id in models.items():
                    for pk, count in prod_id.items():
                        product_type = ContentType.objects.get(app_label=app, model=model)
                        product = product_type.get_object_for_this_type(id=pk)
                        current_decrease = recalculation_with_promo_code(product, promo_code, flag_user_registered)
                        count_prod += count
                        decrease += current_decrease * Decimal(count)

        pattern = re.compile(r'\.[0]+$')
        response = {
            'success': True,
            'count': str(count_prod),
            'amount': pattern.sub('', str(Decimal(specific_amount - decrease).quantize(Decimal('0.01'))))
        }
    else:
        response = {'success': False, 'errors': 'error cart'}

    return JsonResponse(response)


def add_more_product_in_cart(request, app=None, model=None, pk=None):

    if request.is_ajax() and request.method == 'POST':

        pk = int(pk)

        if 'cart' in request.session:
            prod_dict = eval(request.session['cart'])
        else:
            prod_dict = {'prod': {}, 'count': 0, 'amount': Decimal(0)}

        prod_dict['prod'].setdefault(app, {model: {}})
        prod_dict['prod'][app][model].setdefault(pk, 0)
        prod_dict['prod'][app][model][pk] += 1
        prod_dict['count'] += 1
        prod_dict['amount'] = checking_recalculation(prod_dict['prod'])

        request.session['cart'] = repr(prod_dict)

        pattern = re.compile(r'\.[0]+$')

        response = {
            'success': True,
            'count': str(prod_dict['count']),
            'amount': pattern.sub('', str(prod_dict['amount']))
        }
    else:
        response = {'success': False, 'errors': 'error cart'}

    return JsonResponse(response)
