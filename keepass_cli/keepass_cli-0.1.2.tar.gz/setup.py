from distutils.core import setup

install_requires = ['libkeepass']

setup(
  name = 'keepass_cli',
  packages = ['keepass_cli'], # this must be the same as the name above
  entry_points = {
        "console_scripts": ['keepass-cli = keepass_cli.keepass_cli:main']
        },
  version = '0.1.2',
  description = 'A cli interface to keepass/libkeepass',
  author = 'Nathan Huesken',
  author_email = 'nathan.huesken@posteo.de',
  install_requires=install_requires,
  url = 'https://github.com/RudolfVonKrugstein/keepass-cli',
  download_url = 'https://github.com/RudolfVonKrugstein/keepass-cli/tarball/0.1.2',
  classifiers = [
      'Intended Audience :: Developers',
      'Intended Audience :: System Administrators',
      'Operating System :: OS Independent',
      'Topic :: Software Development'
  ],
)
