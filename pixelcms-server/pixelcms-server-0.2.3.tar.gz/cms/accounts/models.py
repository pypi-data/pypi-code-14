from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist

from cms.emails.models import Message


class Account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        on_delete=models.CASCADE
    )

    class Meta:
        app_label = 'accounts'
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return self.user.username

    def send_activation_message(self, request):
        key = signing.dumps({'action': 'ACTIVATE', 'user': self.user.pk})
        link = '<a href="{0}">{0}</a>'.format(
            request.build_absolute_uri(
                '/activate/{}'.format(key)
            )
        )
        content = (
            '<div style="margin-bottom: 20px;">{}</div>\r\n\r\n'
            '<div>{}</div>'
        ).format(
            _('Your accounts has been created. To activate it click on link '
              'below, or copy it to your browser.'), link
        )
        Message.objects.create(
            subject=_('Activate your account'),
            recipients=self.user.email,
            content=content,
            reply_to='no-reply'
        )

    def send_reset_password_message(self, request):
        key = signing.dumps({'action': 'RESET_PASSWORD', 'user': self.user.pk})
        link = '<a href="{0}">{0}</a>'.format(
            request.build_absolute_uri(
                '/reset-password/{}'.format(key)
            )
        )
        content = (
            '<div style="margin-bottom: 20px;">{}</div>\r\n\r\n'
            '<div>{}</div>'
        ).format(
            _('To change you password click on link below, or copy it to your '
              'browser.'), link
        )
        Message.objects.create(
            subject=_('Change your password'),
            recipients=self.user.email,
            content=content,
            reply_to='no-reply'
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_hook(sender, instance, created, **kwargs):
    if created:
        Account.objects.get_or_create(user=instance)


@receiver(post_delete, sender=Account)
def delete_user_hook(sender, instance, **kwargs):
    try:
        instance.user.delete()
    except ObjectDoesNotExist:
        pass
