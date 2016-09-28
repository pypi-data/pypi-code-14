# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
import re
from django.utils import timezone
from django.db.models import Q
from django.db.models import Max

from models import Discount
from views import checking_recalculation


def control_promo_codes(request, promo_code):

    if request.user.is_authenticated():
        flag_user_registered = True
    else:
        flag_user_registered = False

    if 'cart' in request.session:
        prod_dict = eval(request.session['cart'])
        delete_promo_code(prod_dict['prod'], promo_code, flag_user_registered)
        del request.session['cart']


def recalculation_payment(request):

    cart_count = 0
    cart_amount = 0

    if 'cart' in request.session:
        prod_dict = eval(request.session['cart'])
        cart_count = prod_dict['count']
        cart_amount = checking_recalculation(prod_dict['prod'])
        prod_dict['amount'] = cart_amount
        request.session['cart'] = repr(prod_dict)

    return {
        'count': cart_count,
        'amount': cart_amount
    }


# ----------------------------------------------------------

def get_optimal_discount(self):
    current_date = timezone.now().date()
    field_names_dict = self.get_field_names()

    percent_list = [
        self.discount.filter(Q(active=True), Q(use_promo_codes=False),
                             Q(end_date__gt=current_date) | Q(unlimited=True))
            .aggregate(Max('percent'))['percent__max'] or 0
    ]

    for field_name in field_names_dict['foreign_key']:
        field = getattr(self, field_name)
        if field.active:
            percent_list.append(
                field.discount.filter(Q(active=True), Q(use_promo_codes=False),
                                      Q(end_date__gt=current_date) | Q(unlimited=True))
                .aggregate(Max('percent'))['percent__max'] or 0
            )

    for field_name in field_names_dict['many_to_many']:
        field = getattr(self, field_name)
        percent_list.append(
            field.filter(Q(active=True),
                         Q(discount__active=True), Q(discount__use_promo_codes=False),
                         Q(discount__end_date__gt=current_date) | Q(discount__unlimited=True))
            .aggregate(Max('discount__percent'))['discount__percent__max'] or 0
        )

    percent_max = Decimal(max(percent_list))
    self.current_max_percent = percent_max
    return percent_max


def percent_max_promo_code(self, promo_code, flag_user_registered):
    current_date = timezone.now().date()
    field_names_dict = self.get_field_names()
    percent_list = [
        self.discount.filter(Q(active=True),
                             Q(use_promo_codes=True) | Q(use_promo_codes=False),
                             Q(promo_codes__contains=promo_code),
                             Q(only_registered=False) | Q(only_registered=flag_user_registered),
                             Q(end_date__gt=current_date) | Q(unlimited=True))
            .aggregate(Max('percent'))['percent__max'] or 0
    ]

    for field_name in field_names_dict['foreign_key']:
        field = getattr(self, field_name)
        if field.active:
            percent_list.append(
                field.discount.filter(Q(active=True),
                                      Q(use_promo_codes=True) | Q(use_promo_codes=False),
                                      Q(promo_codes__contains=promo_code),
                                      Q(only_registered=False) | Q(only_registered=flag_user_registered),
                                      Q(end_date__gt=current_date) | Q(unlimited=True))
                .aggregate(Max('percent'))['percent__max'] or 0
            )

    for field_name in field_names_dict['many_to_many']:
        field = getattr(self, field_name)
        if field.filter(active=True).count():
            percent_list.append(
                field.filter(Q(active=True),
                             Q(discount__active=True),
                             Q(discount__use_promo_codes=True) | Q(discount__use_promo_codes=False),
                             Q(discount__promo_codes__contains=promo_code),
                             Q(discount__only_registered=False) | Q(discount__only_registered=flag_user_registered),
                             Q(discount__end_date__gt=current_date) | Q(discount__unlimited=True))
                .aggregate(Max('discount__percent'))['discount__percent__max'] or 0
            )

    return Decimal(max(percent_list))


def get_optimal_price(self):
    price = Decimal(self.get_correct_price)
    decrease = (price / Decimal(100)) * self.current_max_discount
    return price - decrease


def recalculation_with_promo_code(self, promo_code, flag_user_registered):
    price = Decimal(self.get_correct_price)
    max_promo_code = percent_max_promo_code(self, promo_code, flag_user_registered)
    if max_promo_code:
        price = (price / Decimal(100)) * max_promo_code
    else:
        price = Decimal(0)
    return price


# For products with a promo code, taken full price
def func_specific_amount(self, promo_code, flag_user_registered):
    price = Decimal(self.get_correct_price)
    max_promo_code = percent_max_promo_code(self, promo_code, flag_user_registered)
    if not max_promo_code:
        price = get_optimal_price(self)
    return price


def delete_promo_code(prod, promo_code, flag_user_registered):
    if promo_code:
        for app, models in prod.items():
            for model, prod_id in models.items():
                for pk in prod_id.keys():
                    product_type = ContentType.objects.get(app_label=app, model=model)
                    product = product_type.get_object_for_this_type(id=pk)
                    percent_max = percent_max_promo_code(product, promo_code, flag_user_registered)
                    content_type_list = [product_type]

                    for item in apps.get_app_config(app).get_models():
                        content_type_list.append(ContentType.objects.get(app_label=app,
                                                                         model=item.__name__.lower()))

                    if percent_max:
                        discounts = Discount.objects.filter(content_type__in=content_type_list,
                                                            active=True,
                                                            use_promo_codes=True,
                                                            not_delete_promo_codes=False,
                                                            percent=Decimal(percent_max),
                                                            promo_codes__contains=promo_code)
                        if discounts:
                            pattern = re.compile(r'(' + promo_code + ')')
                            discount = discounts[0]
                            discount.count_promo_codes -= 1
                            discount.promo_codes = pattern.sub('', discount.promo_codes)
                            discount.save()
                            return None
