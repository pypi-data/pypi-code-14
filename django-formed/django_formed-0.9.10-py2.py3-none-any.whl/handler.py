# coding=utf-8
from __future__ import unicode_literals

try:
    from django.contrib.sites.shortcuts import get_current_site
except:
    from django.contrib.sites.models import get_current_site


from formed.models import FormDefinition, FormSubmission
from formed.utils import import_attribute
from formed.utils.serializing import make_dict_json_serializable
from formed.forms import DefinitionPageForm, DefinitionSummaryForm, DefinitionFinishForm
from formed.settings import FORM_DEFINITION_ID_FIELD, FORM_DEFINITION_PAGE_FIELD, \
    FORM_DEFINITION_PAGE_TYPE_FIELD, FORMED_SESSION_NAME, FORMED_SOURCE_URL_PROVIDER

FORMED_GO_TO_PREVIOUS_PAGE_FIELD = 'form_definition_go_back'
FORMED_PAGE_SUBMISSION_FIELD = 'form_definition_submit'
FORMED_CONFIRM_SUBMISSION_FIELD = 'form_definition_confirm'


class FormDefinitionHandler(object):
    """
    The form definition handler
    """
    form_definition = None

    # Settings to override from the form
    override_definition_settings = {
        'enable_summary': None,
        'finish_text': None,
        'finish_title': None,
        'send_confirmation_email': None,
        'confirmation_email_subject': None,
        'confirmation_email_text': None,
        'confirmation_email_show_summary': None,
        'notification_recipients': None,
    }

    # State
    request = None
    current_form = None
    next_form = None
    current_page = 0
    form_submission = None

    # Instance specific
    source = None

    def __init__(self, request, definition=None, page=None, source=None, **kwargs):
        """
        Initializes the form handler with the given request
        :param request: The request
        :param FormDefinition definition: The FormDefinition instance
        :param int page: The page index
        :param basestring|None source: An optional string which is added to the form submission when the form is saved.
        :param dict kwargs:
        :return:
        """
        self.request = request
        self.request.session.setdefault(FORMED_SESSION_NAME, {})

        if definition is not None:
            self.form_definition = definition
        if page is not None:
            self.current_page = page

        self.source = source

        # Store any override settings:
        self.override_definition_settings.update(
            {setting: kwargs.get(setting) for setting in self.override_definition_settings if setting in kwargs}
        )

        if self.request.method == 'POST':
            if not self.form_definition and FORM_DEFINITION_ID_FIELD in self.request.POST:
                pk = self.request.POST.get(FORM_DEFINITION_ID_FIELD)
                if pk is not None:
                    self.form_definition = FormDefinition.objects.get(pk=pk)
            if not self.current_page and FORM_DEFINITION_PAGE_FIELD in self.request.POST:
                self.current_page = int(self.request.POST.get(FORM_DEFINITION_PAGE_FIELD))

        if self.request and self.form_definition:
            self.handle()

    def handle(self):
        """ Handles the given form definition with the given request. """
        assert self.form_definition is not None, "Cannot handle because no definition is provided."
        self.request.session[FORMED_SESSION_NAME].setdefault(self.form_definition.get_session_key(), {})
        self.request.modified = True
        self.handle_post() if self.request.method == 'POST' else self.handle_get()

    def handle_get(self):
        """ Handles a GET request, the first form page. """
        self.next_form = self.get_form()

    def handle_post(self):
        """ Handles a POST request, going forwards or backwards based on the posted data. """
        current_form = self.get_form(page_type=self.request.POST.get(FORM_DEFINITION_PAGE_TYPE_FIELD, None))

        next_page = None
        going_back = False
        # Forces form validation, making sure that cleaned_data exists
        is_valid = current_form.is_valid()
        # We can always go back:
        if FORMED_GO_TO_PREVIOUS_PAGE_FIELD in self.request.POST:
            # if form.has_previous_page():
            next_page = current_form.get_previous_page()
            going_back = True
            # what if we were going back but get_previous_page returns None?
            # now we ignore this and go to the next page if the page is valid

        if is_valid:
            # first update session:
            if current_form.store_in_session:
                data = self.get_session()
                data.update(
                    make_dict_json_serializable(current_form.cleaned_data)
                )
                self.update_session(data)

            if next_page is None:
                # advance to next page:
                next_page = current_form.get_next_page()

            if next_page is not None:
                # Next form page:
                self.next_form = self.get_form(
                    page=next_page,
                    add_data=not going_back and next_page == self.current_page
                )
            else:
                # There is no next page, should we display a summary?
                summary_enabled = self.form_definition.enable_summary
                if self.override_definition_settings['enable_summary'] is not None:
                    summary_enabled = self.override_definition_settings['enable_summary']

                if summary_enabled and FORMED_CONFIRM_SUBMISSION_FIELD not in self.request.POST:
                    # The next form is the summary page
                    self.next_form = self.get_form(
                        page=self.current_page,
                        page_type='summary',
                        add_data=False
                    )
                    return

                # No summary, so we're saving:
                form_submission = self.save_form()
                if form_submission:
                    # Send the confirmation to the submitter:
                    form_submission.send_confirmation(
                        send_confirmation_email=self.override_definition_settings['send_confirmation_email'],
                        confirmation_email_subject=self.override_definition_settings['confirmation_email_subject'],
                        confirmation_email_text=self.override_definition_settings['confirmation_email_text'],
                        confirmation_email_show_summary=self.override_definition_settings['confirmation_email_show_summary'],
                    )
                    # Send notifications to any configured notification recipients:
                    form_submission.send_notifications(
                        recipients=self.override_definition_settings['notification_recipients']
                    )
                    self.clear_session()

                # The last step is always the finish 'form':
                self.next_form = self.get_form(
                    page=self.current_page,
                    page_type='finish',
                    add_data=False
                )
                return
        else:  # The form is invalid
            if next_page:
                self.next_form = self.get_form(
                    page=next_page
                )
                return

            # The next form is the same form (with errors)
            self.next_form = current_form

    def get_form(self, page_type=None, page=None, add_data=True):
        """
        Returns an instantiated form instance
        :param basestring page_type: The page type for the form
        :param int page: The page index
        :param bool add_data: Whether or not to add data from the request
        """
        form_class = self.get_form_class_by_type(page_type)

        page = self.current_page if page is None else page

        initial = {}
        session_data = self.get_session()
        if session_data:
            initial.update(session_data)

        kwargs = {
            'initial': initial,
            'prefix': None,  # do we want this?
            'form_definition': self.form_definition,
            'form_definition_page': page
        }
        if add_data and self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return form_class(**kwargs)

    @staticmethod
    def get_form_class_by_type(page_type):
        """
        Returns the form class for the given page type
        """
        page_types = {
            'summary': DefinitionSummaryForm,
            'finish': DefinitionFinishForm,
        }
        return page_types.get(page_type) or DefinitionPageForm

    def save_form(self):
        """
        Saves the form submission
        :rtype: FormSubmission|bool
        """
        form_submission = self.get_form_submission()
        if form_submission:
            form_submission.save()
            # All done!
            return form_submission
        # nothing was saved, should we return False or is it ok?
        return False

    def get_form_submission(self):
        """
        Returns a (potentially unsaved) FormSubmission instance for the current state.
        :return:
        """
        if self.form_submission:
            return self.form_submission

        data = self.get_session()
        if data:
            source_url_provider = import_attribute(FORMED_SOURCE_URL_PROVIDER)
            self.form_submission = FormSubmission(
                form_definition=self.form_definition,
                submission=data,
                site=get_current_site(self.request),
                source=self.source,
                source_url=source_url_provider(self.request),
            )
            return self.form_submission
        return None

    def get_context_data(self):
        """
        Returns context data for a template
        :rtype: dict
        """
        page_type = self.get_page_type()
        context = {
            'form_definition': self.form_definition,
            'previous_page_field_name': FORMED_GO_TO_PREVIOUS_PAGE_FIELD,
            'next_page_field_name': self.get_submit_field_name(),
            'form': self.next_form,
        }

        if page_type == 'finish':
            form_submission = self.get_form_submission()
            # finish page settings:
            finish_context = {
                'finish_title': self.override_definition_settings['finish_title'] or self.form_definition.finish_title,
                'finish_text': self.override_definition_settings['finish_text'] or self.form_definition.finish_text,
            }
            if form_submission:  # can potentially be None if the form was already submitted.
                format_context = form_submission.get_text_format_context()
                for key in finish_context:
                    formatted = finish_context[key]
                    try:
                        formatted = finish_context[key].format(**format_context)
                    except KeyError:
                        pass

                    context.update({
                        key: formatted
                    })

        return context

    def get_page_type(self, form=None):
        """
        Returns the normalized page type string
        :rtype: basestring
        """
        form = self.next_form if form is None else form
        if isinstance(form, DefinitionSummaryForm):
            return 'summary'
        if isinstance(form, DefinitionFinishForm):
            return 'finish'
        return 'form'

    def get_submit_field_name(self, form=None):
        """
        Returns the name of the submit button
        :rtype: basestring
        """
        form = self.next_form if form is None else form
        if isinstance(form, DefinitionSummaryForm):
            return FORMED_CONFIRM_SUBMISSION_FIELD
        return FORMED_PAGE_SUBMISSION_FIELD

    def get_session(self):
        """
        Returns the session data
        :rtype: dict
        """
        return self.request.session[FORMED_SESSION_NAME].get(self.form_definition.get_session_key(), None)

    def update_session(self, data):
        """
        Updates session data
        :param dict data: The new session data
        """
        data.pop(FORM_DEFINITION_PAGE_FIELD, None)
        data.pop(FORM_DEFINITION_PAGE_TYPE_FIELD, None)
        data.pop(FORM_DEFINITION_ID_FIELD, None)

        self.request.session[FORMED_SESSION_NAME][self.form_definition.get_session_key()] = data
        self.request.session.modified = True

    def clear_session(self):
        """ Clears the session """
        del self.request.session[FORMED_SESSION_NAME][self.form_definition.get_session_key()]
        self.request.session.modified = True
