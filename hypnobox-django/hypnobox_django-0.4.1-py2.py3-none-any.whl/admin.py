# coding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'email', 'phone_prefix', 'phone_number',
        'product_id', 'media', 'created_on'
    )
    search_fields = (
        'name', 'email', 'phone_prefix', 'phone_number',
        'product_id', 'media',
    )
    date_hierarchy = 'created_on'
