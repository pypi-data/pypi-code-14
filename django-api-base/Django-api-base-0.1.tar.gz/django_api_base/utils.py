import base64
import os
import random
import string
import urllib
import urllib2
import rollbar
import sys
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


# Class for reporting custom message in rollbar
class RollbarCustomReport:
    def __init__(self, message):
        rollbar.report_message(message)


# Class for reporting occured error in rollbar
class RollbarReport:
    def __init__(self):
        rollbar.report_exc_info(sys.exc_info())


def log_me(message):
    logger.info(message)


# Function to generate a random string according to input for ACCESS TOKEN
def generate_access_token(user_id, length=15, chars=string.uppercase + string.digits):
    """
    Generates access token with user_id merged with it for the user
    """
    random_string = random_number_generator(length, chars)
    hashed_value = base64.b16encode(str(user_id))[-2:]
    random_string = "{0}{1}".format(hashed_value, random_string)
    return random_string


# Function for generating random string
def random_number_generator(size, chars=string.lowercase + string.uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# Function for sending template email
def send_template_email(subject, message, to):
    from_email = settings.FROM_EMAIL
    send_mail(subject, message, recipient_list=to, from_email=from_email, html_message=message, fail_silently=True)


# Function for sending OTP
def send_otp(phone_number, otp):
    otp_api = "http://bhashsms.com/api/sendmsg.php?%s"
    dic = {
        "user": os.environ['SMS_USER'],
        "pass": os.environ['SMS_PASSWORD'],
        "sender": "SYMOTP",
        "phone": phone_number,
        "text": otp,
        "priority": "ndnd",
        "stype": "normal",
    }
    data = urllib.urlencode(dic)
    url_caller = urllib2.Request(otp_api % data)
    url_con = urllib2.urlopen(url_caller)
    response = url_con.read()
    log_me(response)
    return 1


# Decorator for checking the permission of the user
def verify_permission(login=True, level=None, login_url='/'):
    """
    :param login: Whether the user has to be login or not
    :param level: Level of the user (None/superuser/staff)
    :param login_url: redirect url
    """

    def verify_permission_view(func):
        def verify(request, *args, **kwargs):
            if login:
                if request.user.is_authenticated():
                    if level is None:
                        pass
                    elif level == 'superuser':
                        if not request.user.is_superuser:
                            return redirect(reverse('404-error-page'))

                    elif level == 'staff':
                        if not request.user.is_staff:
                            return redirect(reverse('404-error-page'))

                    elif level == 'user':
                        if request.user.is_staff or request.user.is_superuser:
                            return redirect(reverse('404-error-page'))
                else:
                    return redirect(login_url)
            else:
                pass

            return func(request, *args, **kwargs)

        return verify

    return verify_permission_view