try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digRegexExtractor',
    'description': 'digRegexExtractor',
    'author': 'Jason Slepicka',
    'url': 'https://github.com/usc-isi-i2/dig-regex-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-regex-extractor',
    'author_email': 'jasonslepicka@gmail.com',
    'version': '0.2.0',
    # these are the subdirs of the current directory that we care about
    'packages': ['digRegexExtractor'],
    'scripts': [],
    'install_requires':['digExtractor>=0.2.0']
}

setup(**config)
