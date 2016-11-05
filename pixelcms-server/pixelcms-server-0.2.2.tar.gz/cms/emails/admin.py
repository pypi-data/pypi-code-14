from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    def html_content(self, obj):
        return obj.content
    html_content.short_description = _('Content')
    html_content.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('subject', 'recipients', 'html_content', 'reply_to',
                    'created', 'sent', 'postdate')
        else:
            return ()

    def get_fieldsets(self, request, obj=None):
        if obj:
            return (
                (None, {
                    'fields': ('subject', 'recipients', 'html_content',
                               'reply_to', ('created', 'sent', 'postdate'))
                }),
            )
        else:
            return (
                (None, {
                    'fields': ('subject', 'recipients', 'content', 'reply_to')
                }),
            )

    list_display = ('subject', 'recipients', 'reply_to', 'created', 'sent',
                    'postdate')
    list_filter = ('sent',)
    search_fields = ('subject', 'recipients', 'reply_to', 'content')

    # fieldsets = (
    #     (None, {
    #         'fields': ('subject', 'recipients', 'content', 'reply_to',
    #                    ('created', 'sent', 'postdate'))
    #     }),
    # )
