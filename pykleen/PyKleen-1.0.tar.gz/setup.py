# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='PyKleen',
      version=open('VERSION').read().strip(),
      packages=['pykleen'],
      url='https://bitbucket.org/creeerio/pykleen',

      author='Nils Corver',
      author_email='nils@creeer.io',
      license='MIT',

      description='Input; simple, clean.',

      classifiers=[
          # 3 - Alpha, 4 - Beta, 5 - Production/Stable
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],

      install_requires=['Werkzeug', 'bleach'],
      setup_requires=['pytest-runner'],
      tests_require=['pytest'])
