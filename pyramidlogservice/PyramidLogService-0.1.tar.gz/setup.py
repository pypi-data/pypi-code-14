import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = [
    'psycopg2',
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
]

tests_requires = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
]

setup(name='PyramidLogService',
      version=0.1,
      description='Pyramid LogService',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords="web services",
      author='Steven Locke',
      author_email='steve.m.locke@gmail.com',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={
          'testing': tests_requires
      })
