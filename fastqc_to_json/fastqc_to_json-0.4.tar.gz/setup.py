#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'fastqc_to_json',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.4,
      description = 'fastqc to json for bwa cwl',
      url = 'https://github.com/jeremiahsavage/fastqc_to_json',
      license = 'Apache 2.0',
      packages = find_packages(),
      install_requires = [
      ],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ],
      entry_points={
          'console_scripts': ['fastqc_to_json=fastqc_to_json.__main__:main']
      },
)
