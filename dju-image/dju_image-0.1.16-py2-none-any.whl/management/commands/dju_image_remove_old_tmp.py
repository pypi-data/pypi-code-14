from django.core.management import CommandError
from dju_common.management import LoggingBaseCommand
from . import profiles_validate
from ...maintenance import remove_old_tmp_files


class Command(LoggingBaseCommand):
    help = 'Remove old temporary uploaded images.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-p', '--profiles', nargs='+',
                            help='Upload profiles. (Default: empty -- all profiles)')
        parser.add_argument('-m', '--max-lifetime', type=int, default=168,
                            help='Time of life file in hours. (Default: 168 (7 days))')

    def handle(self, *args, **options):
        profiles = options['profiles'] or None
        t = profiles_validate(profiles)
        if t:
            raise CommandError(t)
        max_lifetime = options['max_lifetime']
        self.log('Start (profiles: {}; max time of life: {} hours)...'.format(
            ', '.join(profiles) if profiles else '-ALL-',
            max_lifetime,
        ))
        removed, total = remove_old_tmp_files(profiles=profiles, max_lifetime=max_lifetime)
        self.log('Done. Removed: {} / {}'.format(removed, total), double_br=True)
