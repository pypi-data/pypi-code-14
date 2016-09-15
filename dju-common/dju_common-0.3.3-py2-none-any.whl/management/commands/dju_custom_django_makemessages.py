import os
from django.core.management import CommandError
from django.core.management.commands import makemessages


class Command(makemessages.Command):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--add-source-dir', action='append', dest='additional_source_dirs',
                            default=[], metavar='DIR',
                            help='Additional source directory. For example: "/path/to/src:/path/to/locale"')
        parser.add_argument('--no-update-header', action='store_true', dest='no_update_header', default=False,
                            help="Don't update POT-Creation-Date in headers.")

    def handle(self, *args, **options):
        self.additional_source_dirs = options['additional_source_dirs']
        self.no_update_header = options['no_update_header']
        if self.no_update_header:
            try:
                import polib
            except ImportError:
                raise CommandError('Please, install "polib", just run "pip install polib".')
            self.polib = polib
        super(Command, self).handle(*args, **options)

    def find_files(self, root):
        files = super(Command, self).find_files(root)
        for d in self.additional_source_dirs:
            if ':' in d:
                src_dir, locale_dir = d.split(':', 1)
            else:
                src_dir, locale_dir = d, None
            add_files = super(Command, self).find_files(os.path.abspath(src_dir))
            for add_file in add_files:
                add_file.dirpath = os.path.relpath(add_file.dirpath, os.getcwd())
                if locale_dir:
                    add_file.locale_dir = locale_dir
            files.extend(add_files)
        return sorted(files)

    def write_po_file(self, potfile, locale):
        pofile_fn = os.path.join(os.path.dirname(potfile), locale, 'LC_MESSAGES', '{}.po'.format(self.domain))
        old_metadata = {}
        if self.no_update_header and os.path.isfile(pofile_fn) :
            po = self.polib.pofile(pofile_fn)
            old_metadata = po.metadata
            del po
        super(Command, self).write_po_file(potfile, locale)
        if old_metadata:
            po = self.polib.pofile(pofile_fn)
            po.metadata['POT-Creation-Date'] = old_metadata['POT-Creation-Date']
            po.save()
