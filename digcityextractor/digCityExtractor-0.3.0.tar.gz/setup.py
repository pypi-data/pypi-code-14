try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digCityExtractor',
    'description': 'digCityExtractor',
    'author': 'Vinay Rao Dandin',
    'url': 'https://github.com/usc-isi-i2/dig-city-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-city-extractor',
    'author_email': 'vrdandin@isi.edu',
    'version': '0.3.0',
    'install_requires': ['digDictionaryExtractor>=0.3.0', 'digExtractor>=0.3.6'],
    # these are the subdirs of the current directory that we care about
    'packages': ['digCityExtractor'],
    'scripts': [],
}

setup(**config)
