#!/usr/bin/env python

from distutils.core import setup

setup(name='burner-email-providers',
      version='1.2',
      description='Burner Email Providers',
      author='Various Artists',
      author_email='everyone@example.com',
      url='https://github.com/WCF/burner-email-providers/',
      packages=['burner_email_providers'],
      package_data={'burner_email_providers': ['emails.txt']},
     )
