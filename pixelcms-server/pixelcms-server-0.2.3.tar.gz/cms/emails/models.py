import os
from smtplib import SMTPException
import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, get_connection

from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import strip_tags
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    subject = models.CharField(_('subject'), max_length=255)
    recipients = models.TextField(_('recipients'))
    content = models.TextField(_('content'))
    reply_to = models.CharField(_('reply to'), max_length=255)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    sent = models.BooleanField(_('sent'), default=False)
    postdate = models.DateTimeField(_('postdate'), null=True, blank=True)

    class Meta:
        app_label = 'emails'
        ordering = ('-created',)
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return self.subject

    def send(self, connection=None, logger=None):
        if not logger:
            logger = logging.getLogger(__name__)
        msg = EmailMultiAlternatives(
            subject=self.subject,
            body=strip_tags(self.content),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=self.recipients.split(','),
            reply_to=self.reply_to.split(','),
            connection=connection
        )
        msg.attach_alternative(self.content, 'text/html')
        try:
            msg.send()
            self.sent = True
            self.postdate = timezone.now()
            self.save()
            return True
        except (SMTPException, os.error) as e:
            logger.error(
                'Error while sending email (pk: {}): {}'.format(self.pk, e)
            )
            return False

    @classmethod
    def send_awaiting(cls, limit=10):
        awaiting = cls.objects.filter(sent=False).order_by('created')
        sent = 0
        failed = 0
        connection = get_connection()
        logger = logging.getLogger(__name__)
        for msg in awaiting:
            if sent >= limit:
                break
            success = msg.send(connection=connection, logger=logger)
            if success:
                sent += 1
            else:
                failed += 1
        print('Sent: {}\r\nFailed: {}\r\nStill awaiting: {}'.format(
            sent, failed, len(awaiting) - sent
        ))
        connection.close()


@receiver(post_save, sender=Message)
def create_user_hook(sender, instance, created, **kwargs):
    if created:
        instance.send()
