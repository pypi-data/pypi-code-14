from distutils.core import setup
setup(
  name = 'getCDFs',
  py_modules = ['getCDFs'],
  version = '1.0',
  description = 'This will check for cdfs on your computer. If they don\'t exist, or there\'s an updated version on the server, it will download from the server. It will then load the cdfs using spacepy.pycdf, and place them into a dictionary.',
  author = 'Ross Cohen',
  author_email = 'rjc55@njit.edu',
  url = 'https://github.com/BossColo/getCDFs',
  download_url = 'https://github.com/BossColo/getCDFs/tarball/1.0',
  keywords = ['Python', 'spacepy', 'RBSP'],
  classifiers = [],
)