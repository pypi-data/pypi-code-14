import logging

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .models import Message


class ContactFormSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(max_length=255, write_only=True)
    phone = serializers.CharField(
        max_length=255, write_only=True, default=_('(not provided)')
    )
    content = serializers.CharField(max_length=2000, write_only=True)

    def create(self, validated_data):
        logger = logging.getLogger(__name__)
        try:
            recipients = settings.CONTACT_FORM_RECIPIENTS
            if not recipients:
                logger.error('CONTACT_FORM_RECIPIENTS setting is empty.')
        except AttributeError:
            recipients = ''
            logger.error('CONTACT_FORM_RECIPIENTS setting does not exist.')

        content = (
            '<div>{}: <strong>{}</strong></div>\r\n'
            '<div>{}: <strong>{}</strong></div>\r\n'
            '<div style="margin-bottom: 20px;">{}: <strong>{}</strong></div>'
            '\r\n\r\n<div>{}</div>'
        ).format(
            _('Name / company name'), validated_data['name'],
            _('Email address'), validated_data['email'],
            _('Phone number'), validated_data['phone'],
            validated_data['content']
        )

        return Message.objects.create(
            subject=_('Contact form message'),
            recipients=recipients,
            content=content,
            reply_to=validated_data['email']
        )
