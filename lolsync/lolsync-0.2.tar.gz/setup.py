from setuptools import setup
setup(
  name = 'lolsync',
  packages = ['lol_sync'],
  version = '0.2',
  description = 'Keep in sync with friends on League of Legends!',
  author = 'Jason Lin',
  author_email = 'jason_lin2@yahoo.com',
  license = 'MIT',
  url = 'https://github.com/jason2249/LoLSync',
  download_url = 'https://github.com/jason2249/lolsync/tarball/0.2',
  keywords = ['League of Legends', 'Friend', 'Sync'],
  classifiers = [
    'Operating System :: MacOS',
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.4'
  ],
  py_modules=['lol_sync.py'],
  scripts=['lolsync'],
  install_requires = [
    'blessings>=1.6',
    'requests>=2.10.0',
  ]
)