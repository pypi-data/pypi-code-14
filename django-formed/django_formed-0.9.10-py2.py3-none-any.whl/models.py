# coding=utf-8
from __future__ import unicode_literals

import re
from collections import OrderedDict

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import get_language, ugettext_lazy as _
from django.contrib.sites.models import Site
from jsonfield import JSONField

from formed import settings as formed_settings
from formed.form_elements import enforce_field_object
from formed.utils import get_field_display_name
from formed.utils.mail import TemplateMail


class FormDefinitionMixin(object):
    """
    Form definition object
    Contains methods to traverse a form definition stored in it's definition attribute
    """
    definition = {}

    def page_count(self):
        """
        Returns the number of pages in this definition.
        :return:
        """
        return len(self.definition)

    def pages(self):
        """
        Returns all pages in this definition.
        :return:
        """
        return [page for page in self.definition]

    def page(self, page_index):
        """
        Returns the page specified by the given page_index.
        :param int page_index:
        :return:
        """
        return self.definition[page_index]

    def fieldsets(self, page_index=None):
        """
        Returns fieldsets in this definition, optionally filtered by page.
        :param int page_index:
        :return:
        """
        fieldsets = []
        for i, page in enumerate(self.pages()):
            if page_index is None or i == page_index:
                for fieldset in page['fieldsets']:
                    fieldsets.append(fieldset)
        return fieldsets

    def rows(self, page_index=None):
        """
        Returns rows in this definition, optionally filtered by page.
        :param int page_index:
        :return:
        """
        rows = []
        for fieldset in self.fieldsets(page_index=page_index):
            for row in fieldset['rows']:
                rows.append(row)
        return rows

    def fields(self, page_index=None, field_types=None):
        """
        Returns fields in this definition, optionally filtered by page or field type.
        :param int page_index:
        :param list|tuple field_types:
        :return:
        """
        fields = []
        for row in self.rows(page_index=page_index):
            for field_definition in row:
                field = enforce_field_object(field_definition)
                if field_types is None or field['type'] in field_types:
                    fields.append(field)
        return fields

    def has_previous_page(self, current_page=0):
        """
        Returns whether the given page index has a previous page.
        :param current_page:
        :return:
        """
        return current_page != 0

    def has_next_page(self, current_page=0):
        """
        Returns whether the given page index has a next page.
        :param int current_page:
        :return:
        """
        return (current_page + 1) < len(self.pages())

    def get_previous_page(self, data=None, current_page=0):
        """
        Returns the previous page based on the given page index.
        :param dict data:
        :param int current_page:
        :return:
        """
        return current_page - 1 if self.has_previous_page(current_page=current_page) else None

    def get_next_page(self, data=None, current_page=None):
        """
        Returns the index of the next page based on the given data and current page
        :param dict data:
        :param int current_page: Only required if the data does not contain `FORM_DEFINITION_PAGE_FIELD`
        :rtype: int|None
        :return:
        """
        if current_page is None:
            current_page = data.get(formed_settings.FORM_DEFINITION_PAGE_FIELD)

        assert current_page is not None, "No property 'current_page' supplied or no '{}' field found in data.".format(
            formed_settings.FORM_DEFINITION_PAGE_FIELD
        )

        # todo: We simply return the next page. When rules are added we get the next page by applying rules to data.
        next_page = current_page + 1
        return next_page if next_page < len(self.pages()) else None


class FormDefinitionObject(FormDefinitionMixin):
    def __init__(self, definition):
        self.definition = definition


@python_2_unicode_compatible
class FormDefinition(FormDefinitionMixin, models.Model):
    """
    The form definition model.
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    definition = JSONField(_('definition'))
    enable_summary = models.BooleanField(_('enable summary page'), default=True,
                                         help_text=_('Check to enable the summary page which displays an overview of '
                                                     'all submitted data and gives the user the opportunity to double '
                                                     'check their submission.'))
    send_confirmation_email = models.BooleanField(
        _('send confirmation E-mail'), default=True,
        help_text=_('Check to enable sending of a confirmation E-mail to the person who submitted the form. This '
                    'requires an E-mail field to be present in the form. By default the confirmation E-mail field is '
                    'used. If there is none, the value of the first E-mail field will be used.'))
    confirmation_email_subject = models.CharField(
        _('confirmation E-mail subject'), max_length=254, blank=True, null=True,
        help_text=_("The subject of the E-mail that is sent to the person who submitted the form. "
                    "For example: 'Thank you for your message!'. "
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.)."))
    confirmation_email_text = models.TextField(
        _('confirmation E-mail text'), blank=True, null=True,
        help_text=_("The text displayed at the top of the E-mail that is sent to the person who submitted the form. "
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.)."))
    confirmation_email_show_summary = models.BooleanField(_('show field summary in confirmation E-mail'), default=True,
                                                          help_text='Uncheck to hide the submitted fields on the '
                                                                    'confirmation E-mail.')

    notification_email_subject = models.CharField(
        _('notification E-mail subject'), max_length=254, default=_("Submission of the form '{form_name}'"),
        help_text=_("The subject of the E-mail that is sent to the users that are notified of form submissions. "
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.)."))

    finish_title = models.CharField(
        _('finish title'), null=True, blank=True, max_length=255,
        help_text=_("Title displayed on the page if the form is submitted. If left empty "
                    "the default text will be displayed. "
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.)."))
    finish_text = models.TextField(
        _('finish text'), null=True, blank=True,
        help_text=_("Text displayed on the page if the form is submitted. If left empty the "
                    "default text will be displayed. "
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.)."))

    sites = models.ManyToManyField(Site, verbose_name=_('available on'), blank=True,
                                   help_text=_('The sites on which this form is available.'))

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('form')
        verbose_name_plural = _('forms')

    def __str__(self):
        return self.name

    def get_session_key(self):
        return 'u{}'.format(self.pk)

    def clean(self):
        self.definition = [FormDefinition.clean_page(page) for page in self.definition]

    @staticmethod
    def clean_page(page):
        """
        Checks the page for errors by validating it's fieldsets, rows, and fields.
        :param dict page:
        :return:
        """
        page['fieldsets'] = [FormDefinition.clean_fieldset(fieldset) for fieldset in page['fieldsets']]
        return page

    @staticmethod
    def clean_fieldset(fieldset):
        """
        Checks the given fieldset for errors by validating it's rows and fields.
        :param dict fieldset:
        :return:
        """
        fieldset['rows'] = [FormDefinition.clean_row(row) for row in fieldset['rows']]
        return fieldset

    @staticmethod
    def clean_row(row):
        """
        Checks the given row for errors by validating it's fields.
        :param list row:
        :return:
        """
        return [FormDefinition.clean_field(field) for field in row]

    @staticmethod
    def clean_field(field):
        """
        Makes sure all the required attributes are present in the given field or raises ValidationError's for any
        unrecoverable errors.
        :param dict field:
        :return:
        """
        field.setdefault('help_text')
        field.setdefault('type', formed_settings.FORMED_DEFINITION_DEFAULT_FIELD_TYPE)

        error = None
        if 'name' not in field:
            error = ValidationError(_("The %(type)s field with label '%(label)s' has no name."), params={
                'type': get_field_display_name(field.get('type')),
                'label': field.get('label', '')
            })
        elif not re.match(formed_settings.FORMED_NAME_FIELD_REGEX, field.get('name'), re.IGNORECASE):
            error = ValidationError(
                _("The name '%(name)s' of the %(type)s field with label '%(label)s' is invalid. Only letters, numbers, "
                  "- (dash) and the _ (underscore) are allowed."),
                params={
                    'name': field.get('name', ''),
                    'type': get_field_display_name(field.get('type')),
                    'label': field.get('label', '')
                })
        if error is not None:
            import django
            # in Django >= 1.8 we can raise specifically for the definition field.
            raise ValidationError({'definition': error}) if django.VERSION >= 1.8 else error

        return field


@python_2_unicode_compatible
class FormSubmissionNotificationBase(models.Model):
    """ Abstract base class for notification recipients """
    email = models.EmailField(_('E-mail'))
    name = models.CharField(_('name'), max_length=255, blank=True, null=True)
    copy = models.CharField(_('send as copy'), max_length=3, blank=True, null=True, choices=(
        ('cc', _('CC')),
        ('bcc', _('BCC')),
    ))

    class Meta:
        abstract = True
        verbose_name = _('form submission notification recipient')
        verbose_name_plural = _('form submission notification recipients')

    def __str__(self):
        if self.name:
            return self.name
        return self.email


class FormSubmissionNotification(FormSubmissionNotificationBase):
    """ A form submission notification recipient """
    form_definition = models.ForeignKey(FormDefinition, verbose_name=_('form'), on_delete=models.CASCADE)

    class Meta(FormSubmissionNotificationBase.Meta):
        unique_together = (('form_definition', 'email'),)


@python_2_unicode_compatible
class FormSubmission(models.Model):
    """ A form submission """
    form_definition = models.ForeignKey(FormDefinition, verbose_name=_('form'), on_delete=models.CASCADE)
    submission = JSONField(_('submission'))
    site = models.ForeignKey(Site, verbose_name=_('submitted on site'), null=True, blank=True,
                             help_text=_('The site on which the form was submitted.'))
    source = models.CharField(_('source'), max_length=255, null=True, blank=True,
                              help_text=_('This should give you more information on which form this form submission '
                                          'came from.'))
    source_url = models.CharField(_('source page url'), max_length=255, null=True, blank=True,
                                  help_text=_('The URL of the page from which the form was submitted if available.'))
    language = models.CharField(_('language'), default=get_language, max_length=10,
                                help_text=_('The language in which the submitter was using the website when the form '
                                            'was submitted.'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('form submission')
        verbose_name_plural = _('form submissions')

    def __str__(self):
        name = self.get_first_full_name()
        if name:
            return name
        return _("'{form}' form submission").format(form=self.form_definition.name)

    def get_first_full_name(self, as_dict=False):
        """
        Returns the first full name
        :param as_dict: Return as an OrderedDict instead of a space joined string
        :return:
        """
        name_field_keys = {
            'FirstNameField': 'first_name',
            'LastNamePrefixField': 'last_name_prefix',
            'LastNameField': 'last_name'
        }
        name_fields = self.form_definition.fields(field_types=name_field_keys.keys())

        if len(name_fields) > 3:
            # Only get the first 3 fields (here we assume these fields are grouped together for the same name).
            name_fields = name_fields[0:3]

        if len(name_fields) > 0:
            # The order matters:
            name_field_map = OrderedDict([
                ('FirstNameField', ''),
                ('LastNamePrefixField', ''),
                ('LastNameField', ''),
            ])
            # Add the data:
            for field in name_fields:
                if field['name'] in self.submission:
                    name_field_map.update({field['type']: self.submission[field['name']] })

            if as_dict:
                return OrderedDict([
                    # We don't filter out any empty keys to avoid key errors when using as argument for str.format().
                    (name_field_keys[key], name_field_map[key]) for key in name_field_map
                ])

            return ' '.join([value for value in name_field_map.values() if value != ''])
        return None

    get_first_full_name.short_description = _('Full name')

    def get_text_format_context(self):
        """
        Returns a dictionary with information about the form and the submission for use as formatting keys.
        Returned keys are:
        'first_name', 'last_name_prefix', 'last_name', 'full_name', 'form_name', 'submit_language', 'submit_site'
        :rtype: dict
        """
        if hasattr(self, 'text_format_context'):
            return self.text_format_context

        context = {}
        # Add the full name as individual parts:
        full_name_dict = self.get_first_full_name(as_dict=True) or {}
        context.update(full_name_dict)
        full_name = ' '.join(value for value in full_name_dict.values() if value != '')
        context.update({
            # Also add a 'full_name' key:
            'full_name': full_name,
            # Alias for legacy forms:
            'name': full_name,
            # Form definition information:
            'form_name': self.form_definition.name,
            # Form submission information:
            'submit_language': self.language,
            'submit_site': self.site
        })

        self.text_format_context = context

        return context

    def send_confirmation(self, send_confirmation_email=None, confirmation_email_subject=None,
                          confirmation_email_text=None, confirmation_email_show_summary=None):
        """
        Sends a confirmation E-mail to the first EmailField in the definition.
        :param bool|None send_confirmation_email:
        :param str|None confirmation_email_subject:
        :param str|None confirmation_email_text:
        :param bool|None confirmation_email_show_summary:
        :return:
        """
        if send_confirmation_email is True or (
                    send_confirmation_email is None and self.form_definition.send_confirmation_email
        ):
            # todo: We could add a field which sets whether or not the user wants to receive a notification?

            # Get all ConfirmationEmailFields from the definition or fall back to EmailFields
            email_fields = self.form_definition.fields(
                field_types=('ConfirmationEmailField',)
            ) or self.form_definition.fields(field_types=('EmailField',))
            if len(email_fields) > 0:
                # Get the value of the first EmailField:
                to_email = self.submission[email_fields[0]['name']]

                # We know it's a valid e-mail due to form validation, only check if it's not empty
                # (it could be that the field is not required).
                if to_email:
                    format_context = self.get_text_format_context()
                    subject = (confirmation_email_subject or self.form_definition.confirmation_email_subject or '')
                    try:
                        subject = subject.format(**format_context)
                    except KeyError:
                        pass
                    show_summary = confirmation_email_show_summary
                    if confirmation_email_show_summary is None:
                        show_summary = self.form_definition.confirmation_email_show_summary

                    text = confirmation_email_text or self.form_definition.confirmation_email_text or ''
                    try:
                        text = text.format(**format_context)
                    except KeyError:
                        pass

                    context = {
                        'form_definition': self.form_definition,
                        'form_submission': self,
                        'subject': subject,
                        'text': text,
                        'show_summary': show_summary,
                    }
                    # Also add all the formatting context variables to the context:
                    context.update(format_context)

                    mail = TemplateMail(
                        subject=subject,
                        context=context,
                        template_name='form_definition/email/confirmation'
                    )
                    return mail.send(to=[to_email], from_email=formed_settings.FORMED_NOTIFICATION_FROM_EMAIL)
        return None

    def send_notifications(self, recipients=None):
        """
        Send notification E-mails
        :param list|None recipients:
        :return:
        """
        if recipients is None:
            recipients = self.form_definition.formsubmissionnotification_set.all()
        elif callable(recipients):
            recipients = recipients()

        if len(recipients) > 0:
            context = {
                'form_definition': self.form_definition,
                'form_submission': self,
            }
            format_context = self.get_text_format_context()
            context.update(format_context)
            send = {
                'to': None,
                'cc': None,
                'bcc': None,
                'from_email': formed_settings.FORMED_NOTIFICATION_FROM_EMAIL
            }

            for recipient in recipients:
                field = 'to'
                if recipient.copy and recipient.copy in send:
                    field = recipient.copy

                if send[field] is None:
                    send[field] = []

                address_format = '{name} <{email}>' if recipient.name else '{email}'
                send[field].append(address_format.format(name=recipient.name, email=recipient.email))

            subject = self.form_definition.notification_email_subject
            if not subject:
                subject = formed_settings.FORMED_NOTIFICATION_DEFAULT_SUBJECT

            try:
                subject = subject.format(**format_context)
            except KeyError:
                pass

            mail = TemplateMail(
                subject=subject,
                context=context,
                template_name='form_definition/email/notification'
            )
            return mail.send(**send)
        return None
