from distutils.core import setup
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        install.run(self)
        print("RUNNING CUSTOM SCRIPT")
        print(os.getcwd())

setup(
  name = 'easy_sqlite',
  packages = ['easy_sqlite'], # this must be the same as the name above
  version = '1.0.13',
  description = 'This Library makes using the sqlite3 library much easier and faster.',
  author = 'Calder White',
  author_email = 'calderwhite1@gmail.com',
  url = 'https://github.com/CalderWhite/easy_sqlite', # use the URL to the github repo
  download_url = 'https://github.com/CalderWhite/easy_sqlite/archive/master.zip', # I'll explain this in a second
  keywords = [], # arbitrary keywords
  classifiers = [],
  cmdclass={
        'install': CustomInstallCommand,
    }
)
