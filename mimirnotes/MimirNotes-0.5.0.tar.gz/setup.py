from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(name='MimirNotes',
      version='0.5.0',
      description='A simple, command line, note taking utility.',
      long_description=long_description,
      keywords='note terminal command-line journal',
      url='https://github.com/jcerise/mimir',
      author='Jeremy Cerise',
      author_email='jcerise06@gmail.com',
      packages=['MimirNotes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['click', 'enum34', 'dateparser'],
      entry_points='''
            [console_scripts]
            mimir=MimirNotes.mimir:cli
      ''',
      )
