from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string


class Command(BaseCommand):
	help = 'Generate a new Django secret key'

	def handle(self, *args, **options):
		characters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = get_random_string(50, characters)
		self.stdout.write(self.style.SUCCESS(key))