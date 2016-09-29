# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()


def main():
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'testapp.tests.test'])


if __name__ == '__main__':
    main()
