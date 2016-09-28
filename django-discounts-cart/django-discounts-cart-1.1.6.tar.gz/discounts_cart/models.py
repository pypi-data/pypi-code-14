# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError

from decimal import Decimal
from django.utils import timezone
import re
import random

from django.db.models import Max
from django.db.models import Q

import operator

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


@python_2_unicode_compatible
class Discount(models.Model):

    percent = models.DecimalField(_('Percent discount'), max_digits=4, decimal_places=2, default=0.0,
                                  help_text=_('Example: 5 or 0,05'))
    start_date = models.DateField(_('Start date'), default=timezone.now)
    end_date = models.DateField(_('End date'), null=True, blank=True,
                                help_text=_('For unlimited, not necessary'))

    # Promo-code
    promo_codes = models.TextField(_('Promo-codes'), blank=True, default='',
                                   help_text=_('In this field, it will be generated promo-codes'))
    use_promo_codes = models.BooleanField(_('Use promo-codes ?'), default=False)
    count_promo_codes = models.PositiveSmallIntegerField(_('Count promo-codes'), default=0, blank=True)
    only_registered = models.BooleanField(_('Only registered users ? - (Promo-codes)'), default=False)
    not_delete_promo_codes = models.BooleanField(_('Not delete promo-codes ?'), default=False)
    # End - Promo-code

    unlimited = models.BooleanField(_('Unlimited ? - (Date)'), default=False)
    active = models.BooleanField(_('Active discount'), default=True)

    content_type = models.ForeignKey(ContentType,  on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        pattern = re.compile(r'\.[0]+$')
        return '{} %'.format(pattern.sub('', str(self.percent)))

    class Meta:
        ordering = ('start_date', 'id')
        verbose_name = _('Discount')
        verbose_name_plural = _('Discounts')

    def view_percent(self):
        pattern = re.compile(r'\.[0]+$')
        return '{} %'.format(pattern.sub('', str(self.percent)))
    view_percent.short_description = _('Percent discount')

    def clean(self):
        percent = self.percent
        start_date = self.start_date
        end_date = self.end_date
        unlimited = self.unlimited
        errors = {}

        if Decimal(percent).is_zero():
            raise ValidationError({'percent': _('Not be zero')})
        elif Decimal(percent).is_signed():
            errors['percent'] = _('Only positive numbers')

        if not unlimited and start_date:
            current_date = timezone.now().date()
            if not end_date:
                errors['end_date'] = _('End date must not be blank')
            elif not (end_date > current_date):
                errors['end_date'] = _('End date must be greater than the current date')
            elif not (start_date < end_date):
                errors['start_date'] = _('Start date must be less than the end date')

        if errors is not None:
            raise ValidationError(errors)


# Abstract models
class DiscountsInCategories(models.Model):

    # Discount group ----------------
    discount = GenericRelation(Discount)

    def view_percent_discount(self):
        pattern = re.compile(r'\.[0]+$')
        current_date = timezone.now().date()
        percent_max = self.discount.filter(Q(active=True), Q(use_promo_codes=False),
                                           Q(end_date__gt=current_date) | Q(unlimited=True)
                                           ).aggregate(Max('percent'))['percent__max'] or 0

        return '{} %'.format(pattern.sub('', str(percent_max)))
    view_percent_discount.short_description = _('Maximum discount')
    # End - Discount group ----------

    class Meta:
        abstract = True


class TotalQuerySet(models.QuerySet):

    def active(self):
        return self.filter(active=True)

    def sort(self):
        return self.filter(active=True)


class TotalManager(models.Manager):

    def get_queryset(self):
        return TotalQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def sort_by_optimal_discount(self):
        products = list(self.get_queryset().sort())
        products.sort(key=operator.attrgetter('current_max_discount'), reverse=True)
        return products


class DiscountsInProducts(DiscountsInCategories):

    objects = models.Manager()
    products = TotalManager()

    class Meta:
        abstract = True

    current_max_discount = models.DecimalField(_('Current max percent'), max_digits=4,
                                               decimal_places=2, default=0.0)

    current_optimal_price = models.DecimalField(_('current_optimal_price'), max_digits=10,
                                                decimal_places=2, default=0)

    # Discount group ----------------
    # extra method for calculation of optimal prices

    def view_optimal_discount(self):
        pattern = re.compile(r'\.[0]+$')
        return pattern.sub('', str(self.current_max_discount))

    def view_optimal_price(self):
        pattern = re.compile(r'\.[0]+$')
        return pattern.sub('', str(self.current_optimal_price.quantize(Decimal('0.01'))))
    # End - Discount group ----------


# signals
flag_save_promo_codes = False


def generate_promo_codes(instance, **kwargs):
    global flag_save_promo_codes
    flag_save_promo_codes = True

    if instance.use_promo_codes and instance.count_promo_codes and \
            not len(instance.promo_codes):
        temp = ''
        allowed_chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        count_chars = len(allowed_chars)
        count_promo_codes = instance.count_promo_codes
        num = 0
        num_2 = 0

        while num < count_promo_codes:
            while num_2 < 12:
                temp += allowed_chars[random.randrange(count_chars)]
                num_2 += 1
            instance.promo_codes += '{}\n'.format(temp)
            temp = ''
            num += 1
            num_2 = 0
        else:
            pattern = re.compile(r'[\n]+$')
            instance.promo_codes = pattern.sub('', instance.promo_codes)
        instance.save()
    elif not instance.use_promo_codes and len(instance.promo_codes):
        instance.promo_codes = ''
        instance.count_promo_codes = 0
        instance.save()
    elif not instance.use_promo_codes and instance.count_promo_codes:
        instance.count_promo_codes = 0
        instance.save()
    elif instance.use_promo_codes and not instance.count_promo_codes:
        instance.use_promo_codes = False
        instance.save()

    # recalculation of optimal discount and optimal price
    from utils import get_optimal_discount, get_optimal_price

    product_type = ContentType.objects.get(app_label=instance.content_type.app_label,
                                           model='product')
    product_class = product_type.model_class()

    for product in product_class.objects.all():
        product.current_max_discount = get_optimal_discount(product)
        product.current_optimal_price = get_optimal_price(product)
        product.save()

    flag_save_promo_codes = False

post_save.connect(generate_promo_codes,  sender=Discount)


@receiver(post_save)
def update_product(sender, instance, **kwargs):
    from django.apps import apps
    from utils import get_optimal_discount, get_optimal_price

    if not flag_save_promo_codes and sender.__name__ == 'Product':
        product_model = apps.get_model(sender._meta.label)
        product = product_model.objects.get(id=instance.id)

        max_discount = instance.current_max_discount = get_optimal_discount(product)
        optimal_price = instance.current_optimal_price = get_optimal_price(product)

        if product.current_max_discount != max_discount or \
                product.current_optimal_price != optimal_price:
            instance.save()
