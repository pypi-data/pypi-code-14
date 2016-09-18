"""
Project Views
"""

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from ..models import Environment
from ..tools.codec import decode_key, encrypt

# pylint: disable=unused-argument
def view(request, identifier):
    "Example view"
    environment = get_object_or_404(Environment, ident=identifier)
    data = environment.get_variables()
    rsa_key = decode_key(environment.envar)[1]
    encrypted = encrypt(rsa_key, data)
    return HttpResponse(content=encrypted)

