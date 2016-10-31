"""
Project Views
"""

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from cenvars import api
from ..models import Environment


# pylint: disable=unused-argument
def view(request, identifier):
    "Example view"
    environment = get_object_or_404(Environment, ident=identifier)
    data = environment.get_variables()
    rsa_key = api.decode_key(environment.envar)[-1]
    encrypted = api.encrypt(rsa_key, data)
    return HttpResponse(content=encrypted)
