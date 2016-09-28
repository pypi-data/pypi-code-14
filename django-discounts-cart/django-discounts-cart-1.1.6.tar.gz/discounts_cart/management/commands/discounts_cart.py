# -*- coding: utf-8 -*-
from django.core.management import BaseCommand, CommandError
from django.utils import timezone

from ...models import Discount


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('action')

    def handle(self, *args, **options):
        current_date = timezone.now().date()
        # Deactivate used discounts
        if options['action'] == 'deact':
            Discount.objects.filter(unlimited=False,
                                    end_date__lte=current_date).update(active=False)
        # Delete used discounts
        elif options['action'] == 'del':
            Discount.objects.filter(unlimited=False,
                                    end_date__lte=current_date).delete()
