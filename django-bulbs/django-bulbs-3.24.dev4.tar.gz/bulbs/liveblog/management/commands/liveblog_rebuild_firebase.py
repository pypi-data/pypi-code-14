import requests

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Set a provided FeatureType as available for Facebook Instant Articles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--liveblog",
            help="Rebuild specific liveblog cache",
            type=int
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            default=False,
            help='Verbose mode')

    def handle(self, *args, **options):

        LiveBlog = apps.get_model(settings.LIVEBLOG_MODEL)

        qs = LiveBlog.objects.all()

        if options['liveblog']:
            qs = qs.filter(pk=options['liveblog'])

        for liveblog in qs.all():

            endpoint = settings.LIVEBLOG_FIREBASE_NOTIFY_ENTRIES_ENDPOINT
            url = endpoint.format(liveblog_id=liveblog.id)

            if liveblog.is_published:

                entries = {}
                for e in liveblog.entries.all():
                    entries[e.id] = {'id': e.id}

                    if e.published:
                        entries[e.id]['published'] = e.published.isoformat()

                if options['verbose']:
                    self.stdout.write('Rebuild LiveBlog {} ({} entries)'.format(liveblog.id,
                                                                                len(entries)))
                    self.stdout.write(url)

                resp = requests.put(url, json=entries)
            else:
                if options['verbose']:
                    self.stdout.write('Delete unpublished LiveBlog {} entries'.format(liveblog.id))
                resp = requests.delete(url)

            resp.raise_for_status()
