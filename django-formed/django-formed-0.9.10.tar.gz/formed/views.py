# coding=utf-8
from __future__ import unicode_literals
import os

from django.views.generic import TemplateView

from formed.handler import FormDefinitionHandler
from formed.settings import FORM_DEFINITION_ID_FIELD
from formed.models import FormDefinition


class FormDefinitionView(TemplateView):
    """
    A simple TemplateView based class which uses the FormDefinitionHandler to display a form.
    """

    # The path in which the templates are located
    template_path = 'form_definition'
    # The format for a template file, override if you, for example, use a different file extension
    template_name_format = '{}.html'

    # Form handler instance, set in get_context_data
    form_handler = None

    # Form definition
    _form_definition = None

    def post(self, request, *args, **kwargs):
        """ Our POST entry point is exactly the same as our GET. """
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        This is where the 'magic' happens. Our form handler is initialised and handles the current request. When done
        we simply add the context data from the handler to our context data.
        :param dict kwargs: Request kwargs
        :return:
        """
        context = super(FormDefinitionView, self).get_context_data(**kwargs)

        self.form_handler = FormDefinitionHandler(**self.get_definition_handler_settings())
        context.update(self.form_handler.get_context_data())

        return context

    def get_definition_handler_settings(self):
        """
        Returns keyword arguments for the form definition handler.
        Override this to modify definition handler settings.
        :return:
        """
        return {
            'request': self.request,
            'definition': self.get_form_definition(),
            # 'enable_summary': True,  # Override whether or not to enable the summary view
            # 'finish_title': None,  # Override the finish title
            # 'finish_text': None,  # Override the finish text
            # 'source': None,  # Override this field to differentiate different sources of the same form
            # 'send_confirmation_email': True,  # Override whether or not to send the confirmation email
            # 'send_confirmation_email': True,  # Override whether or not to send the confirmation email
            # 'confirmation_email_subject': None,  # Override the confirmation email subject
            # 'confirmation_email_text': None,  # Override the confirmation email text
            # 'notification_recipients': None,  # Override the notification recipients with a list of FormSubmissionNotification instances.
        }

    def get_form_definition(self, pk=None):
        """
        Returns a FormDefinition instance for the given pk or based on the current request.
        Override this if you have a different method of determining the current form definition.
        :param pk:
        :rtype: FormDefinition
        """
        if self._form_definition is not None and (pk is None or self._form_definition.pk == pk):
            return self._form_definition
        if pk is None:
            if self.request.method == 'POST':
                pk = self.request.POST.get(FORM_DEFINITION_ID_FIELD)
            else:
                pk = self.kwargs.get('pk')
        self._form_definition = FormDefinition.objects.get(pk=pk)
        return self._form_definition

    def get_template_names(self):
        """
        Returns the template names
        :rtype: list
        """
        template = self.form_handler.get_page_type()
        return [os.path.join(self.template_path, self.template_name_format.format(template))]
