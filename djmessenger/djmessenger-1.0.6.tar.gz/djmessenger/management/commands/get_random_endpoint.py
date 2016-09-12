from django.core.management.base import BaseCommand
import os, binascii


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(binascii.hexlify(os.urandom(25)))
