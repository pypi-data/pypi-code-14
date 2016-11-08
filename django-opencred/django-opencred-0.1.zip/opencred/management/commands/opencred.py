import itertools
import json

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from opencred.settings import SETTINGS


class Command(BaseCommand):
    help = 'OpenCred.io password reuse identification'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action="count", help="Do not print information on each user. " +
                                                                  "Use twice to print nothing at all.")

    @staticmethod
    def get_all_user_ids():
        for user in get_user_model().objects.all():
            # TODO cache user objects
            if hasattr(user, 'username') and user.username:
                yield str(user.pk), user.username
            if hasattr(user, 'email') and user.email:
                yield str(user.pk), user.email
                yield str(user.pk), user.email.split('@')[0]

    @staticmethod
    def get_all_user_id_chunks():
        user_iterator = Command.get_all_user_ids()
        while True:
            users_chunk = list(itertools.islice(user_iterator, 100))
            if users_chunk:
                yield users_chunk
            else:
                break

    def get_all_passwords_to_try(self):
        api_session = requests.session()
        for user_ids_chunk in Command.get_all_user_id_chunks():
            req = api_session.post('https://api.opencred.io/v1/lookup/',
                                   headers={
                                       'X-API-Key': SETTINGS.OPENCRED_API_KEY,
                                       'Content-Type': 'application/json',  # old requests doesn't support json=...
                                   },
                                   data=json.dumps(user_ids_chunk))

            if req.status_code != 200:
                self.stdout.write(self.style.ERROR('API call failed: %s' % req.text))
                break

            user_password_tuples = {}

            for pk, passwords in req.json():
                if pk not in user_password_tuples:
                    user = get_user_model().objects.get(pk=pk)
                    user_password_tuples[pk] = (user, passwords['passwords'])
                else:
                    user_password_tuples[pk][1].extend(passwords['passwords'])

            for user, passwords in user_password_tuples.values():
                yield user, passwords

    def handle(self, *args, **options):
        opencred_group, _ = Group.objects.get_or_create(name=SETTINGS.OPENCRED_RESTRICTED_GROUP)

        for user, passwords in self.get_all_passwords_to_try():
            for password in passwords:
                if user.check_password(password):
                    user.groups.add(opencred_group)
                    if options['quiet'] < 2:
                        self.stdout.write(self.style.ERROR('%s is reusing a password!' % user))
                    break
            else:
                if options['quiet'] < 1:
                    self.stdout.write(self.style.SUCCESS('%s is safe' % user))
