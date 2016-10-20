from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'A build system (for sass, javascript, ...).'

    def add_arguments(self, parser):
        parser.add_argument('-w', '--watch', dest='watch',
                            required=False, action='store_true',
                            help='Starts a blocking process that watches for changes.')
        parser.add_argument('-a', '--appnames', dest='appnames',
                            required=False, default=None, nargs='*',
                            help='Specify one or more apps to build. If not specified, all '
                                 'apps are built. Example: "--appnames ievv_jsbase demoapp2"')

    def handle(self, *args, **options):
        appnames = options['appnames']
        if appnames:
            try:
                settings.IEVVTASKS_BUILDSTATIC_APPS.validate_appnames(appnames=appnames)
            except ValueError as error:
                self.stderr.write(str(error))
                raise SystemExit()
        settings.IEVVTASKS_BUILDSTATIC_APPS.log_help_header()
        settings.IEVVTASKS_BUILDSTATIC_APPS.configure_logging()
        settings.IEVVTASKS_BUILDSTATIC_APPS.install(appnames=appnames)
        settings.IEVVTASKS_BUILDSTATIC_APPS.run(appnames=appnames)
        if options['watch']:
            settings.IEVVTASKS_BUILDSTATIC_APPS.watch(appnames=appnames)
