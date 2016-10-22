from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import (
    get_default_password_validators
)

from .models import Account


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class RegisterSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'[a-zA-Z0-9\-_]',
        min_length=3,
        max_length=30
    )
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)

    def validate_username(self, val):
        user = Account.objects.filter(user__username=val).exists()
        if user:
            raise serializers.ValidationError(
                _('Provided username is already taken.')
            )
        return val

    def validate_email(self, val):
        user = Account.objects.filter(user__email=val).exists()
        if user:
            raise serializers.ValidationError(
                _('Provided email address is already taken.')
            )
        return val

    def validate_password(self, val):
        validators = get_default_password_validators()
        for v in validators:
            v.validate(val)
        return val

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_('Passwords do not match.'))
        return data


class ActivateSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)


class ResendActivationMessageSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class SendResetPasswordMessageSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class ResetPasswordSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    password2 = serializers.CharField(max_length=255)

    def validate_password(self, val):
        validators = get_default_password_validators()
        for v in validators:
            v.validate(val)
        return val

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(_('Passwords do not match.'))
        return data
