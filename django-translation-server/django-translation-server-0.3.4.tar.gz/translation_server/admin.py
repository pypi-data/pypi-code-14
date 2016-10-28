from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from django.conf import settings
from translation_server.models import *
from translation_server.forms import *


class CustomModelAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdminMixin, self).__init__(model, admin_site)
        self.filter_horizontal = [field.name for field in model._meta.get_fields() if
                                  field.many_to_many and "reverse" not in str(type(field))]


@admin.register(TranslationType)
class TranslationTypeAdmin(TabbedTranslationAdmin):
    pass


@admin.register(Translation)
class TranslationAdmin(TabbedTranslationAdmin):
    form = TranslationAdminForm
    fieldsets = (
        ('Translation type', {
            'fields': ('type',)
        }),
        ('Primary info', {
            'fields': ('tag', 'text')
        }),
        ('Auxiliary info', {
            'fields': ('auxiliary_tag', 'auxiliary_text')
        }),
    )
    list_display = ('tag', 'type', 'text')

    class Media:
        import os
        js_dir = os.path.join(settings.STATIC_URL, 'admin/js')
        js = (
            js_dir + '/admin-translation.js',
        )

