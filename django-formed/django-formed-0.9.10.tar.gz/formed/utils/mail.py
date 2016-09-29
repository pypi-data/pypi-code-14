# coding=utf-8
from __future__ import unicode_literals
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class TemplateMail(object):
    """
    Simple template based mailer
    """
    template_name = None
    context = None
    subject = None

    def __init__(self, context=None, template_name=None, subject=None):
        """
        Creates a new Mail
        :param subject:
        :param context:
        :return:
        """
        self.set_context(context)
        self.set_template_name(template_name)
        self.set_subject(subject)

    def set_context(self, context):
        """
        Set the context of the mail
        :param context:
        :return:
        """
        self.context = context

    def set_subject(self, subject):
        """
        Sets the subject of the mail
        :param subject:
        :return:
        """
        self.subject = subject

    def set_template_name(self, template_name):
        """
        Set the template name (without extension)
        :param template_name:
        :return:
        """
        self.template_name = template_name

    def send(self, to=None, cc=None, bcc=None, from_email=None):
        """
        Renders the templates and sends the mail
        :param from_email:
        :param to:
        :param cc:
        :param bcc:
        :return:
        """
        # Render te templates
        text = render_to_string('{}.txt'.format(self.template_name), self.context)
        html = render_to_string('{}.html'.format(self.template_name), self.context)

        mail = EmailMultiAlternatives(subject=self.subject, body=text, to=to, cc=cc, bcc=bcc,
                                      from_email=settings.DEFAULT_FROM_EMAIL if from_email is None else from_email)
        mail.attach_alternative(html, 'text/html')
        return mail.send()
