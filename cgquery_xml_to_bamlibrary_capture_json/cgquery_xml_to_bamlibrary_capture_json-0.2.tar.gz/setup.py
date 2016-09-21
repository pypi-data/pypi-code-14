#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name = 'cgquery_xml_to_bamlibrary_capture_json',
      author = 'Jeremiah H. Savage',
      author_email = 'jeremiahsavage@gmail.com',
      version = 0.2,
      description = 'convert cgquery sra xml to capture_kits/target_set json',
      url = 'https://github.com/jeremiahsavage/cgquery_xml_to_bamlibrary_capture_json/',
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
          'console_scripts': ['cgquery_xml_to_bamlibrary_capture_json=cgquery_xml_to_bamlibrary_capture_json.__main__:main']
      }
)
