from django.contrib import admin
from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from polymorphic.admin import (
    PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
)

from cms.common import mixins
from .models import Page, PageCategory, PageArticle, PageCustomComponent


BASE_READONLY_FIELDSETS = ()
BASE_FIELDSETS = (
    (None, {
        'fields': (
            'title', 'slug', 'published', 'order', 'homepage',
            'react_component_name', 'language'
        )
    }),
)


class PageCategoryAdmin(PolymorphicChildModelAdmin):
    base_model = PageCategory
    raw_id_fields = ('category',)
    autocomplete_lookup_fields = {'fk': ['category']}

    readonly_fields = BASE_READONLY_FIELDSETS
    fieldsets = BASE_FIELDSETS + (
        (_('Category page'), {
            'fields': ('category',)
        }),
    )


class PageArticleAdmin(PolymorphicChildModelAdmin):
    base_model = PageArticle
    raw_id_fields = ('article',)
    autocomplete_lookup_fields = {'fk': ['article']}

    readonly_fields = BASE_READONLY_FIELDSETS
    fieldsets = BASE_FIELDSETS + (
        ('Article page', {
            'fields': ('article',)
        }),
    )


class PageCustomComponentAdmin(PolymorphicChildModelAdmin):
    base_model = PageCustomComponent

    readonly_fields = BASE_READONLY_FIELDSETS
    fieldsets = BASE_FIELDSETS + mixins.SeoAdmin.fieldsets


@admin.register(Page)
class PageAdmin(PolymorphicParentModelAdmin):
    base_model = Page
    child_models = [
        (import_string(model), import_string(admin_model))
        for (model, admin_model) in settings.PAGE_TYPES
    ]

    def page_type(self, obj):
        return obj.get_real_instance_class()._meta.verbose_name
    page_type.short_description = _('Page type')

    def all_routes(self, obj):
        return '<br />'.join(
            '<a href="{0}">{0}</a>'.format(r) for r in obj.all_routes
        )
    all_routes.short_description = _('Routes')
    all_routes.allow_tags = True

    list_display = ('title', 'page_type', 'all_routes', 'published', 'order',
                    'homepage', 'language')
    list_filter = ('published', 'homepage', 'language')
    list_editable = ('published', 'order', 'language')
    search_fields = ('title',)
