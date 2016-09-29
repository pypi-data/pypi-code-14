# coding=utf-8
import os

from django.views.generic import TemplateView
from cmsplugin_formed_form.models import Form
from cmsplugin_formed_form.cms_plugins import FORMED_CMSPLUGIN_TEMPLATE_PATH
from formed.handler import FormDefinitionHandler


class CMSPluginFormedFormView(TemplateView):

    form_handler = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """ Handles the form and returns context data for the rendered form """
        context = super(CMSPluginFormedFormView, self).get_context_data(**kwargs)

        instance = Form.objects.get(pk=kwargs.get('form_id'))
        context['instance'] = instance

        self.form_handler = FormDefinitionHandler(
            request=self.request,
            definition=instance.form_definition,
            enable_summary=instance.get_enable_summary(),
            finish_title=instance.finish_title or None,
            finish_text=instance.finish_text or None,
            source=instance.source or None,
            send_confirmation_email=instance.get_send_confirmation_email(),
            confirmation_email_subject=instance.confirmation_email_subject or None,
            confirmation_email_text=instance.confirmation_email_text or None,
            notification_recipients=instance.get_notification_recipients,
            confirmation_email_show_summary=instance.get_confirmation_email_show_summary(),
        )

        context.update(self.form_handler.get_context_data())
        return context

    def get_template_names(self):
        template = self.form_handler.get_page_type()
        return [
            os.path.join(FORMED_CMSPLUGIN_TEMPLATE_PATH, '{}.html'.format(template))
        ]
