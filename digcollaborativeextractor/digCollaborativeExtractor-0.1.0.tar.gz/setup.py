try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digCollaborativeExtractor',
    'description': 'digCollaborativeExtractor',
    'author': 'Majid Ghasemi-Gol',
    'url': 'https://github.com/usc-isi-i2/dig-collaborative-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-dictionary-extractor',
    'author_email': 'ghasemig@gmail.com',
    'version': '0.1.0',
    'install_requires': ['digExtractor>=0.3.2'],
    # these are the subdirs of the current directory that we care about
    'packages': ['digCollaborativeExtractor'],
    'scripts': [],
}

setup(**config)
