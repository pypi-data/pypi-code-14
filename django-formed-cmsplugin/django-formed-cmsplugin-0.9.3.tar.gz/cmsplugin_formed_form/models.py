# coding=utf-8
from __future__ import unicode_literals

from itertools import chain
from django.utils.translation import ugettext_lazy as _
from django.db import models
from cms.models import CMSPlugin
from formed.models import FormDefinition, FormSubmissionNotificationBase

BOOLEAN_NO, BOOLEAN_YES, BOOLEAN_INHERIT = 0, 1, -1
BOOLEAN_CHOICES = (
    (BOOLEAN_INHERIT, _('Inherit from form definition')),
    (BOOLEAN_YES, _('Yes')),
    (BOOLEAN_NO, _('No')),
)


class Form(CMSPlugin):
    """
    The form model which contains settings for the form definition.
    """
    form_definition = models.ForeignKey(FormDefinition)

    # Source field:
    source = models.CharField(_('source'), max_length=255, null=True, blank=True,
                              help_text=_("This should give more information about the page and location from which "
                                          "this form is submitted. Can be anything from a number or 'Bottom form on "
                                          "product page X'."))
    # Override settings from the form:
    enable_summary = models.SmallIntegerField(
        _('enable summary page'), null=True, default=BOOLEAN_INHERIT, choices=BOOLEAN_CHOICES,
        help_text=_('Check to enable the summary page which displays an overview of all submitted data and gives the '
                    'user the opportunity to double check their submission.'))
    send_confirmation_email = models.SmallIntegerField(
        _('send confirmation E-mail'), default=BOOLEAN_INHERIT, choices=BOOLEAN_CHOICES, null=True,
        help_text=_('Check to enable sending of a confirmation E-mail to the person who submitted the form. This '
                    'requires an E-mail field to be present in the form. By default the value of the first E-mail '
                    'field will be used.'))
    confirmation_email_subject = models.CharField(
        _('confirmation E-mail subject'), max_length=254, blank=True, null=True,
        help_text=_("The subject of the E-mail that is sent to the person who submitted the form. "
                    "For example: 'Thank you for your message!' "
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.).")
    )
    confirmation_email_text = models.TextField(
        _('confirmation E-mail text'), blank=True, null=True,
        help_text=_("The text displayed at the top of the E-mail that is sent to the person who submitted the form. "
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.).")
    )
    confirmation_email_show_summary = models.SmallIntegerField(
        _('show field summary in confirmation E-mail'), null=True, default=BOOLEAN_INHERIT, choices=BOOLEAN_CHOICES,
        help_text='Uncheck to hide the submitted fields on the confirmation E-mail.'
    )
    notification_email_subject = models.CharField(
        _('notification E-mail subject'), max_length=254, null=True, blank=True,
        help_text=_("The subject of the E-mail that is sent to the users that are notified of form submissions. "
                    "Possible placeholders are {name} (form name), {language} (user language) and {site} (the site)."
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.).")
    )
    inherit_submission_notifications = models.BooleanField(
        _('inherit notification recipients?'), default=True,
        help_text=_("Uncheck if you don't want to inherit the notification recipients from the form. Only the "
                    "recipients added to this plugin are used.")
    )
    finish_title = models.CharField(
        _('finish title'), null=True, blank=True, max_length=255,
        help_text=_("Title displayed on the page if the form is submitted. "
                    "If left empty the default text will be displayed."
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.)."))
    finish_text = models.TextField(
        _('finish text'), null=True, blank=True,
        help_text=_("Text displayed on the page if the form is submitted. If left empty the "
                    "default text will be displayed."
                    "Possible placeholders are: {first_name}, {last_name_prefix}, {last_name} or {full_name} (the "
                    "users name, when available in the form), {form_name}, {submit_language} (user language) and "
                    "{submit_site} (the site from which the form was submitted.)."))

    def get_enable_summary(self):
        """
        Returns the actual boolean value whether to enable the summary page.
        :rtype: bool
        """
        if self.enable_summary == BOOLEAN_INHERIT:
            return self.form_definition.enable_summary
        return self.enable_summary == BOOLEAN_YES

    def get_confirmation_email_show_summary(self):
        """
        Returns the actual boolean value whether to enable the summary in the confirmation E-mail.
        :rtype: bool
        """
        if self.confirmation_email_show_summary == BOOLEAN_INHERIT:
            return self.form_definition.confirmation_email_show_summary
        return self.confirmation_email_show_summary == BOOLEAN_YES

    def get_send_confirmation_email(self):
        """
        Returns the actual boolean value whether to send the confirmation e-mail.
        :rtype: bool
        """
        if self.send_confirmation_email == BOOLEAN_INHERIT:
            return self.form_definition.send_confirmation_email
        return self.send_confirmation_email == BOOLEAN_YES

    def get_notification_recipients(self):
        """
        Lazy way of getting the notification recipients which are only required when actually sending the
        notifications.
        :return:
        """
        # Get the recipients configured with the plugin:
        notification_recipients = self.formpluginsubmissionnotification_set.all()
        if self.inherit_submission_notifications:
            # We are also inheriting form the form definition, append those:
            plugin_recipients = self.form_definition.formsubmissionnotification_set.all()
            notification_recipients = list(chain(plugin_recipients, notification_recipients))
        return notification_recipients


class FormPluginSubmissionNotification(FormSubmissionNotificationBase):
    form_definition = models.ForeignKey(Form, verbose_name=_('form'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('(Additional) form submission notification recipient')
        verbose_name_plural = _('(Additional) form submission notification recipients')
