from django.contrib.auth import (
    get_user_model, authenticate, login as perform_login,
    logout as perform_logout
)
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core import signing

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    LoginSerializer, RegisterSerializer, ActivateSerializer,
    ResendActivationMessageSerializer, SendResetPasswordMessageSerializer,
    ResetPasswordSerializer
)
from .models import Account


@api_view(['GET', 'DELETE'])
def authInfo(request):
    if request.method == 'GET':
        # auth info will be attached by AuthInfoMiddleware
        return Response(status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        perform_logout(request)
        return Response(
            status=status.HTTP_200_OK,
            data={'msg': _('You have been logged out.')}
        )


@api_view(['POST'])
def login(request):
    if request.user.is_authenticated():
        return Response(
            status=status.HTTP_200_OK,
            data={'msg': _('You have been logged in.')}
        )
    else:
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            # get username
            username_or_email = serializer.data['username_or_email']
            if '@' in username_or_email:
                try:
                    username = Account.objects \
                        .get(user__email=username_or_email).user.username
                except Account.DoesNotExist:
                    username = username_or_email
            else:
                username = username_or_email

            # try credentials
            user = authenticate(
                username=username,
                password=serializer.data['password']
            )
            if user is not None:
                perform_login(request, user)
                return Response(
                    status=status.HTTP_200_OK,
                    data={'msg': _('You have been logged in.')}
                )
        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={'_error': _('Wrong username or password.')}
        )


@api_view(['POST'])
def register(request):
    if request.user.is_authenticated():
        return Response(
            status=status.HTTP_200_OK,
            data={
                'msg': _('You are already logged in.')
            }
        )
    else:
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_user_model().objects.create_user(
                username=serializer.data['username'],
                email=serializer.data['email'],
                password=serializer.data['password']
            )
            if settings.ACCOUNTS_ACTIVATION:
                user.is_active = False
                user.save()
                user.account.send_activation_message(request)
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        'activation': True,
                        'msg': _('Your account has been created. Activation '
                                 'message has been sent to provided email '
                                 'address.')
                    }
                )
            else:
                user = authenticate(
                    username=serializer.data['username'],
                    password=serializer.data['password']
                )
                perform_login(request, user)
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={
                        'msg': _('You account has been created. You are '
                                 'logged in.')
                    }
                )


@api_view(['POST'])
def activate(request):
    serializer = ActivateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        invalid_key_response = Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'_error': _('Activation key is invalid.')}
        )
        try:
            key_data = signing.loads(serializer.data['key'], max_age=60*60)
            if key_data.get('action') != 'ACTIVATE':
                return invalid_key_response
            try:
                user = get_user_model().objects.get(pk=key_data['user'])
                if not user.is_active:
                    user.is_active = True
                    user.save()
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={'msg': _('Your account is now active. You can log '
                                   'in.')}
                )
            except get_user_model().DoesNotExist:
                return invalid_key_response
        except signing.SignatureExpired:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'expired': True,
                    '_error': _('Activation key has expired.')
                }
            )
        except signing.BadSignature:
            return invalid_key_response


@api_view(['POST'])
def resend_activation_message(request):
    serializer = ResendActivationMessageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = get_user_model().objects.get(
                email=serializer.data['email'],
                is_active=False
            )
            user.account.send_activation_message(request)
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'msg': _('Activation message has been sent to provided '
                             'email address.')
                }
            )
        except get_user_model().DoesNotExist:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'_error': _('Provided email is not associated with any '
                                  'account that needs to be activated.')}
            )


@api_view(['POST'])
def send_reset_password_message(request):
    serializer = SendResetPasswordMessageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            user = get_user_model().objects.get(email=serializer.data['email'])
            user.account.send_reset_password_message(request)
            return Response(
                status=status.HTTP_201_CREATED,
                data={
                    'msg': _('Message with instructions how to change your '
                             'password has been sent to provided email '
                             'address.')
                }
            )
        except get_user_model().DoesNotExist:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={'_error': _('Provided email is not associated with any '
                                  'account.')}
            )


@api_view(['POST'])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        invalid_key_response = Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                'keyError': True,
                '_error': _('Change password key is invalid.')
            }
        )
        try:
            key_data = signing.loads(serializer.data['key'], max_age=60*60)
            if key_data.get('action') != 'RESET_PASSWORD':
                return invalid_key_response
            try:
                user = get_user_model().objects.get(pk=key_data['user'])
                user.set_password(serializer.data['password'])
                user.save()
                user = authenticate(
                    username=user.username,
                    password=serializer.data['password']
                )
                perform_login(request, user)
                return Response(
                    status=status.HTTP_201_CREATED,
                    data={'msg': _('Your password has been changed. You are '
                                   'logged in.')}
                )
            except get_user_model().DoesNotExist:
                return invalid_key_response
        except signing.SignatureExpired:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'keyError': True,
                    '_error': _('Change password key has expired.')
                }
            )
        except signing.BadSignature:
            return invalid_key_response
