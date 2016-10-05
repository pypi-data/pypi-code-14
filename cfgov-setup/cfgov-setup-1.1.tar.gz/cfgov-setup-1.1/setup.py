import os
from setuptools import setup


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

setup(name='cfgov-setup',
      version='1.1',
      py_modules='cfgov_setup',
      url='https://github.com/cfpb/cfgov-django-setup',
      maintainer= 'CFPB',
      maintainer_email='tech@cfpb.gov',
      long_description=read_file('README.md'),
      entry_points={'distutils.setup_keywords':
               ['frontend_build_script=cfgov_setup:do_frontend_build']
           }
      )
