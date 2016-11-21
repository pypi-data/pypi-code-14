from django.contrib import admin

from .models import NavModule, NavModuleItem

from cms.common import mixins


class NavModuleItemInline(admin.StackedInline):
    model = NavModuleItem
    extra = 0
    sortable_field_name = 'order'
    raw_id_fields = ('page',)
    autocomplete_lookup_fields = {'fk': ['page']}

    fieldsets = (
        (None, {
            'fields': ('name', 'page', 'scroll_to_element',
                       ('link', 'link_open_in_new_tab'), 'published', 'order')
        }),
    )


@admin.register(NavModule)
class NavModuleAdmin(mixins.ModuleAdmin):
    list_display = ('name', 'published', 'template_id', 'language')
    list_filter = ('published', 'language')
    list_editable = ('published', 'language')
    search_fields = ('name',)

    inlines = (NavModuleItemInline,)
