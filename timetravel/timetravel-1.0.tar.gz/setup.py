import sys
from setuptools import setup

from timetravel import __version__
from timetravel import __doc__ as description

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    with open('README.md') as file:
        long_description = file.read()

setup(name='timetravel',
      version=__version__,
      author='bmweiner',
      author_email='bmweiner@users.noreply.github.com',
      url='https://github.com/bmweiner/timetravel',
      description=description,
      long_description=long_description,
      classifiers = [
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Office/Business :: Office Suites',
          'Topic :: Office/Business :: Scheduling',
          'Topic :: Text Processing :: General',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
      platforms=['py27', 'py35'],
      license='MIT License',
      packages=['timetravel'])
