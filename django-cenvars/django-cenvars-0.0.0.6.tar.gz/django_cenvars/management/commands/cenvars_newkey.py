"""
Command update languages.
"""
import rsa
from django.conf import settings
from django.core.management.base import BaseCommand
from ...tools import codec

def create():
    "create key"
    _,key = rsa.newkeys(settings.RSA_KEYSIZE)
    # need to split this out in a encode/decode key
    _, tmp = codec.encode_key(key, url=settings.DEFAULT_SERVER)
    return tmp


class Command(BaseCommand):
    """Create a new server key pair."""
    help = "Create a new server key pair."

    # pylint: disable=unused-argument
    def handle(self, *args, **kwargs):
        return create()

