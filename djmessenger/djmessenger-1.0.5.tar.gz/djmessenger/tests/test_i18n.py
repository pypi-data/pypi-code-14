# -*- coding: utf-8 -*-
from django.test import TestCase


class TestI18N(TestCase):
    def test_basic(self):
        import gettext

        zh = gettext.translation('django',
                                 localedir='/Volumes/HDD/Dropbox/Personal/Projects/djmessenger/djmessenger/locale',
                                 languages=['zh'])
        zh.install()
        print(_('Thanks for your message'))
