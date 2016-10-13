#!/usr/bin/env python
import os

from distutils.core import setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
        SCRIPT_DIR = os.getcwd()

# put together list of requirements to install
install_requires = []
with open(os.path.join(SCRIPT_DIR, 'requirements.txt')) as fh:
    for line in fh.readlines():
        if line.startswith('-'):
            continue

        install_requires.append(line.strip())

data_files = []

setup(name='zymbit-connect',
      version='2.0.1',
      description='Zymbit Connect',
      author='Roberto Aguilar',
      author_email='roberto@zymbit.com',
      package_dir={'': 'src'},
      packages=[
          'zymbit',
          'zymbit.connect',
          'zymbit.upstream',
          'zymbit.util',
      ],
      scripts=[
          'src/scripts/connect',
          'src/scripts/write_auth_token',
      ],
      data_files=data_files,
      long_description=open('README.md').read(),
      url='http://zymbit.com/',
      license='LICENSE',
      install_requires=install_requires,
)
