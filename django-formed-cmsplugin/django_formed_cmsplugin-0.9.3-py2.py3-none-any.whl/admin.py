# coding=utf-8
from django.contrib import admin
from formed.models import FormDefinition
from formed.admin import FormDefinitionAdmin, FormSubmissionNotificationInline
from cmsplugin_formed_form.models import FormPluginSubmissionNotification
from cms.admin.placeholderadmin import PlaceholderAdminMixin


class FormPluginSubmissionNotificationInline(FormSubmissionNotificationInline):
    model = FormPluginSubmissionNotification


class CMSFormDefinitionAdmin(PlaceholderAdminMixin, FormDefinitionAdmin):
    pass

admin.site.unregister(FormDefinition)
admin.site.register(FormDefinition, CMSFormDefinitionAdmin)
