try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digDictionaryExtractor',
    'description': 'digDictionaryExtractor',
    'author': 'Jason Slepicka',
    'url': 'https://github.com/usc-isi-i2/dig-dictionary-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-dictionary-extractor',
    'author_email': 'jasonslepicka@gmail.com',
    'version': '0.2.1',
    'install_requires': ['pygtrie', 'digExtractor>=0.2.0'],
    # these are the subdirs of the current directory that we care about
    'packages': ['digDictionaryExtractor'],
    'scripts': [],
}

setup(**config)
