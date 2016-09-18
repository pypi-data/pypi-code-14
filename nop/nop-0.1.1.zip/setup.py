from distutils.core import setup
import nop

setup(
  name = 'nop',
  packages = ['nop'], # this must be the same as the name above
  version = nop.version_string,
  description = 'Package for no-op object, useful for testing stuff without changing logic',
  author = 'invhndl',
  author_email = 'invalidhandle@outlook.com',
  url = 'https://bitbucket.org/invalidhandle/nop',
  download_url = 'https://bitbucket.org/invalidhandle/nop/get/{}.tar.gz'.format(nop.version_string),
  keywords = ['nop', 'testing', 'no-op', 'nothing'],
  classifiers = ['Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3'],
  license='MIT'
)