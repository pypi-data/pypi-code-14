#!/usr/bin/env python
# encoding: utf-8


from setuptools import setup, find_packages
version = '0.2.0'
classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    ("Topic :: Software Development :: "
     "Libraries :: Python Modules")
]

setup(name="flask-tmpl",
      version=version,
      description="PasteScript templates for the Flask+Celery+SQLAlchemy",
      classifiers=classifiers,
      keywords='flask paste templates',
      author='yetship',
      author_email='liqianglau@outlook.com',
      url='https://liuliqiang.info/docs/flask-tmpl',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['flask'],
      include_package_data=True,
      install_requires=['setuptools', 'PasteScript'],
      entry_points="""
        # -*- Entry points: -*-
         [paste.paster_create_template]
        flask-tmpl=flask.skels.package:Package
      """
)
