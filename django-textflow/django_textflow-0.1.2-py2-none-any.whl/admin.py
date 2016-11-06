from django.contrib import admin

try:
    from modeltranslation.admin import TranslationAdmin
    ADMIN_MODEL = TranslationAdmin
except ImportError:
    TranslationAdmin = admin.ModelAdmin
    ADMIN_MODEL = TranslationAdmin

from textflow.models import FlowObject
# Register your models here.


class FlowObjectAdmin(ADMIN_MODEL):
    fields = ('text',)

    list_display = ['text']
    list_filter = ['text']
    search_fields = ['text']


admin.site.register(FlowObject, FlowObjectAdmin)
