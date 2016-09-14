from setuptools import setup, find_packages
import sys, os

version = '1.2.4'

setup(name='pydipankar',
      version=version,
      description="Common lib used by Dipoankar",
      long_description="""\
Common lib used by dipankar""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='dipankar spider common lib experimenet',
      author='dipankar',
      author_email='ddutta@microsoft.com',
      url='',
      license='',
      #version='1.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      data_files=['simplestore_index.html'],    
      #package_dir={'pydipankar': 'pydipankar'},
      #package_data={'pydipankar': ['data/*.dat']},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-i
          'requests',
          'fake_useragent',
          'beautifulsoup4',
          'tornado',
          'pymongo'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
