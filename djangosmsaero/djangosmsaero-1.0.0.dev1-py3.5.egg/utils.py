# -*- coding: utf-8 -*-

import re
import logging
import requests
from hashlib import md5
from django_rq import job
# from urllib import quote_plus
from django.utils.html import strip_tags
from smsaero import conf as settings
from .models import Signature
from .models import SMSMessage

logger = logging.getLogger('smsaero')


class SmsSender():
    PROTOCOL = 'http'
    HOST = 'gate.smsaero.ru'

    def send_request(self, params, link):
        params['user'] = settings.SMSAERO_USER
        params['password'] = self._get_password()
        # params['answer'] = 'json'

        url = 'https://gate.smsaero.ru/{}'.format(link)

        try:
            response = requests.get(url, params)
            return response.text
        except:
            return 'connection_error'

    def _get_password(self):
        if settings.SMSAERO_PASSWORD_MD5:
            return settings.SMSAERO_PASSWORD_MD5

        m = md5()
        m.update(settings.SMSAERO_PASSWORD.encode())
        return m.hexdigest()

    def parse_response(self, response):
        if '=' in response:
            return response.split('=')
        return response, None

    def get_signature(self, signature_id=None):
        if signature_id:
            try:
                return Signature.objects.get(pk=signature_id)
            except Signature.DoesNotExist:
                pass
        else:
            try:
                return Signature.objects.all()[0]
            except IndexError:
                pass
        return


sender = SmsSender()


def send_sms(phone, text, signature_id=None, date=None, link='/send/'):

    match = re.search('^\+?\d{11}$', phone)
    if not match:
        Exception('Not valid phone')
        return

    signature = sender.get_signature(signature_id)
    if not signature:
        Exception('Have not not one signature')
        return

    params = {
        'to': phone,
        'text': text,
        'from': signature.name,
    }
    if date:
        params['date'] = date
    response = sender.send_request(params, link)
    sms_id, status = sender.parse_response(response)

    if not sms_id or not status:
        msg = 'Can not send SMS to %s. Status: %s' % (phone, sms_id)
        logger.error(msg)
        raise Exception(msg)

    sms = SMSMessage(
        phone=phone,
        signature=signature,
        text=text,
        sms_id=sms_id,
        status=status,
    )
    sms.save()
    return sms


def get_sms_status(sms_id, link='/status/'):
    response = sender.send_request({'id': sms_id}, link)
    sms_id, status = sender.parse_response(response)
    return status


def get_balance(link='/balance/'):
    response = sender.send_request({}, link)
    stuff, balance = sender.parse_response(response)
    return balance


def get_signatures_name(link='/senders/'):
    response = sender.send_request({}, link)
    return [n for n in response.split('\n') if n]


@job('default')
def send_sms_async(*args, **kwargs):
    return send_sms(*args, **kwargs)


@job('default')
def get_sms_status_async(*args, **kwargs):
    return get_sms_status(*args, **kwargs)


@job('default')
def get_balance_async(*args, **kwargs):
    return get_balance(*args, **kwargs)


@job('default')
def get_signatures_name_async(*args, **kwargs):
    return get_signatures_name(*args, **kwargs)
