from django.contrib import admin

from .models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('language', 'site_name', 'meta_description', 'meta_robots')

    fieldsets = [
        (None, {
            'fields': ('language', 'site_name',
                       ('page_title_site_name_suffix', 'suffix_separator'),
                       'meta_description', 'meta_robots')
        }),
    ]
