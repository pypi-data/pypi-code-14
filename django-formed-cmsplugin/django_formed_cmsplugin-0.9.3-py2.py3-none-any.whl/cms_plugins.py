# coding=utf-8
import os

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from cmsplugin_formed_form.admin import FormPluginSubmissionNotificationInline
from cmsplugin_formed_form.models import Form
from formed.handler import FormDefinitionHandler


FORMED_CMSPLUGIN_TEMPLATE_PATH = getattr(settings, 'FORMED_CMSPLUGIN_TEMPLATE_PATH', 'plugins/formed_form/')


class FormPlugin(CMSPluginBase):
    name = _('Form')
    model = Form
    cache = False
    radio_fields = {
        'enable_summary': admin.HORIZONTAL,
        'send_confirmation_email': admin.HORIZONTAL,
    }
    fieldsets = (
        (None, {
            'fields': [
                'form_definition',
                'source',
            ]
        }),
        (_('After submitting the form...'), {
            'fields': [
                'enable_summary',
                'finish_title',
                'finish_text',
            ]
        }),
        (_('Confirmation E-mail'), {
            'classes': ('collapse',),
            'fields': [
                'send_confirmation_email',
                'confirmation_email_show_summary',
                'confirmation_email_subject',
                'confirmation_email_text',
            ]
        }),
        (_('Notification E-mail'), {
            'classes': ('collapse',),
            'fields': [
                'notification_email_subject',
                'inherit_submission_notifications',
            ]
        }),
    )
    inlines = (FormPluginSubmissionNotificationInline,)

    # Instance
    form_handler = None

    def get_render_template(self, context, instance, placeholder):
        template = self.form_handler.get_page_type()
        return os.path.join(FORMED_CMSPLUGIN_TEMPLATE_PATH, '{}.html'.format(template))

    def render(self, context, instance, placeholder):
        """
        Returns the context for the Form plugin
        :param dict context:
        :param Form instance:
        :param str placeholder:
        :return:
        """
        context = super(FormPlugin, self).render(context, instance, placeholder)

        self.form_handler = FormDefinitionHandler(
            request=context.get('request'),
            definition=instance.form_definition,
            enable_summary=instance.get_enable_summary(),
            finish_title=instance.finish_title or None,
            finish_text=instance.finish_text or None,
            source=instance.source or None,
            send_confirmation_email=instance.get_send_confirmation_email(),
            confirmation_email_show_summary=instance.confirmation_email_show_summary or None,
            confirmation_email_subject=instance.confirmation_email_subject or None,
            confirmation_email_text=instance.confirmation_email_text or None,
            notification_recipients=instance.get_notification_recipients,
        )

        context.update(self.form_handler.get_context_data())
        return context


plugin_pool.register_plugin(FormPlugin)
