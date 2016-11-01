"""
setup packaging script for validate-yaml
"""

import os

version = "0.0"
dependencies = ['PyYAML']

# allow use of setuptools/distribute or distutils
kw = {}
try:
    from setuptools import setup
    kw['entry_points'] = """
      [console_scripts]
      validate-yaml = validateyaml.main:main
"""
    kw['install_requires'] = dependencies
except ImportError:
    from distutils.core import setup
    kw['requires'] = dependencies

try:
    here = os.path.dirname(os.path.abspath(__file__))
    description = file(os.path.join(here, 'README.txt')).read()
except IOError:
    description = ''


setup(name='validate-yaml',
      version=version,
      description="validate yaml",
      long_description=description,
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      author='Jeff Hammel',
      author_email='k0scist@gmail.com',
      url='',
      license='',
      packages=['validateyaml'],
      include_package_data=True,
      zip_safe=False,
      **kw
      )
