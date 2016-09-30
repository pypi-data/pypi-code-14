# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import QueuedContent, Metadata, ContentMetadata
from splitjson.widgets import SplitJSONWidget
from jsonfield import JSONField


class QueuedContentAdmin(admin.ModelAdmin):
    '''
    Admin View for QueuedItem
    '''
    list_display = ('content_type', 'object_id', 'bibblio_id', 'status')
    list_filter = ('content_type', )
    raw_id_fields = ('bibblio_id', )
    readonly_fields = ('status_info', )

admin.site.register(QueuedContent, QueuedContentAdmin)


class MetadataAdmin(admin.ModelAdmin):
    '''
    Admin View for Metadata
    '''
    list_display = ('text', 'type', 'ignore')
    list_filter = ('type', )
    search_fields = ('text', )

    formfield_overrides = {
        JSONField: {'widget': SplitJSONWidget},
    }

admin.site.register(Metadata, MetadataAdmin)


class ContentMetadataAdmin(admin.ModelAdmin):
    '''
    Admin View for ContentMetadata
    '''
    list_display = ('metadata', 'relevance_bar', 'ignore')
    list_filter = ('metadata__type', )

    def relevance_bar(self, obj):
        from django.template import Context
        from django.template.loader import get_template
        if obj.relevance is not None:
            relevance = "%d%%" % (obj.relevance / 10.0)
        else:
            relevance = False

        tmpl = get_template("admin/bibblio/relevancebar.html")
        ctxt = Context({'relevance': relevance})
        return tmpl.render(ctxt)
    relevance_bar.allow_tags = True
    relevance_bar.admin_order_field = 'relevance'
    relevance_bar.short_description = 'Relevance'

    class Media:
        css = {'all': ('bibblio/relevancebar.css', )}

admin.site.register(ContentMetadata, ContentMetadataAdmin)
