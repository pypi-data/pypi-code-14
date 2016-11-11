"""
This management command is to provide a convenient way to get a random string
act as the REST endpoint.

You just need to invoke this management command and then copy/paste the string
provided to :data:`djmessenger.settings.DJM_ENDPOINT`
"""
from django.core.management.base import BaseCommand
import os, binascii


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(binascii.hexlify(os.urandom(25)))
