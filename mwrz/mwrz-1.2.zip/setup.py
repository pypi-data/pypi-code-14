from distutils.core import setup

setup(
  name = 'mwrz',
  packages=['mwrz'],# this must be the same as the name above
  version = '1.2',
  # scripts=['mwrz/fastpypi.py'],
  description = "it just make basic dirs and files and a little text for creating a pypi package",
  long_description="help you faster,Run : fastpypi --packagename hello",
  author = 'treelake',
  author_email = 'author_email@gmail.com',
  url = 'http://github_package', # use the URL to the github repo
  download_url = 'http://github_can_download_package',
  keywords = [], # arbitrary keywords
  classifiers = [],
  install_requires = ['easyargs', ''], # dependencies needed
  license="Apache-2.0",
  entry_points = {
        'console_scripts': [
            'fastpypi = mwrz.fastpypi:main'
        ]
  },
)
