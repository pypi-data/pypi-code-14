"""
Command update languages.
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from cenvars import api

def create():
    "create key"
    return api.create_key(url=settings.DEFAULT_SERVER,
                          key_size=settings.RSA_KEYSIZE)

class Command(BaseCommand):
    """Create a new server key pair."""
    help = "Create a new server key pair."

    # pylint: disable=unused-argument
    def handle(self, *args, **kwargs):
        return create()
