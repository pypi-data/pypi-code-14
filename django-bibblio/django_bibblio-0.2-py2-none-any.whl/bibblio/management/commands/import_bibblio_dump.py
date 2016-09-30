from django.core.management.base import LabelCommand, CommandError


class Command(LabelCommand):
    help = "Import a JSON dump from Bibblio"
    missing_args_message = "import_bibblio_dump requires a file path to import"

    def handle_label(self, label, **options):
        import os
        import json
        from bibblio import importer

        if not os.path.exists(label):
            raise CommandError("%s does not exist." % label)

        with open(label) as f:
            self.stdout.write("Opening %s" % label)
            data = json.loads(f.read())
            i = 0
            for record in data:
                i += 1
                if i % 5 == 0:
                    self.stdout.write("Importing record %s" % i)
                importer.process_record(record)
