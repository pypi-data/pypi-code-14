# coding: utf-8
from __future__ import unicode_literals, print_function
from django.utils.http import urlencode

SPECS = {}


def register(cls):
    SPECS[cls.VERSION] = cls


def get_spec():
    from .settings import SPEC_VERSION
    return SPECS[SPEC_VERSION]()


class SpecBase(object):

    def get_chat_url(self, instance):
        from .settings import CLIENT_ID, DOMAIN

        params = self.get_params(instance)
        url = self.CHAT_URL.format(
            client_id=CLIENT_ID,
            domain=DOMAIN,
            params=urlencode(params)
        )
        return url


@register
class Spec12(SpecBase):
    VERSION = 1.2
    CHAT_URL = 'http://{client_id}.{domain}/?controle=Atendimento&acao=entrar&{params}'

    def get_params(self, instance):
        return dict(
            nome=instance.name,
            email=instance.email,
            ddd_residencial=instance.phone_prefix,
            tel_residencial=instance.phone_number,
            id_produto=instance.product_id,
            midia=instance.media,
        )


@register
class Spec10(SpecBase):
    VERSION = 1.0
    CHAT_URL = 'http://{client_id}.{domain}/atendimento/entrar.php?acao=ENTRAR&{params}'

    def get_params(self, instance):
        return dict(
            nome=instance.name,
            email=instance.email,
            ddd_residencial=instance.phone_prefix,
            tel_residencial=instance.phone_number,
            id_produto=instance.product_id,
            referencia=instance.media,
        )
