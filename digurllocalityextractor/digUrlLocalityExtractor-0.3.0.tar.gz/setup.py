try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digUrlLocalityExtractor',
    'description': 'digUrlLocalityExtractor',
    'author': 'Vinay Rao Dandin',
    'url': 'https://github.com/usc-isi-i2/dig-url-locality-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-url-locality-extractor',
    'author_email': 'vrdandin@isi.edu',
    'version': '0.3.0',
    'install_requires': ['digDictionaryExtractor>=0.3.0',
                         'digExtractor>=0.3.6',
                         'digCityExtractor'],
    # these are the subdirs of the current directory that we care about
    'packages': ['digUrlLocalityExtractor'],
    'scripts': [],
}

setup(**config)
