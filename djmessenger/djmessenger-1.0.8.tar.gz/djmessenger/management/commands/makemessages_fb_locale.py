# -*- coding: utf-8 -*-
"""
This management command will perform makemessages for all locales defined by
Facebook
"""
from django.core.management.base import BaseCommand
from django.core.management.commands import makemessages
import xmltodict
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        file = os.path.join(os.path.dirname(__file__),
                            './FacebookLocales.xml')
        if not os.path.exists(file):
            raise IOError('FacebookLocales.xml not found in %s' % file)
        locales = []
        with open(file) as fd:
            doc = xmltodict.parse(fd.read())
            for locale in doc['locales']['locale']:
                representation = locale['codes']['code']['standard']['representation']
                locales.append(representation)
        makemessages.Command().handle(
            **{
                'locale': locales,
                'exclude': [],
                'domain': 'django',
                'all': False,
                'extensions': [],
                'symlinks': False,
                'ignore': [],
                'no-default-ignore': True,
                'no_wrap': False,
                'no_location': False,
                'no_obsolete': False,
                'keep_pot': False,
                'verbosity': 1,
                'ignore_patterns': [],
                'use_default_ignore_patterns': True
            }
        )
