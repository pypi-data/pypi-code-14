try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digReadabilityExtractor',
    'description': 'digReadabilityExtractor',
    'author': 'Jason Slepicka',
    'url': 'https://github.com/usc-isi-i2/dig-readability-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-readability-extractor',
    'author_email': 'jasonslepicka@gmail.com',
    'version': '0.1',
    # these are the subdirs of the current directory that we care about
    'packages': ['digReadabilityExtractor'],
    'scripts': [],
}

setup(**config)
