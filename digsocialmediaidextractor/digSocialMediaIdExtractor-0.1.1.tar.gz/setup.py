try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digSocialMediaIdExtractor',
    'description': 'digSocialMediaIdExtractor',
    'author': 'Rahul Kapoor',
    'url': 'https://github.com/usc-isi-i2/dig-socialmedia-id-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-socialmedia-id-extractor',
    'author_email': 'rahulkap@isi.edu',
    'version': '0.1.1',
    'install_requires': ['digExtractor>=0.2.0'],
    # these are the subdirs of the current directory that we care about
    'packages': ['digSocialMediaIdExtractor'],
    'scripts': [],
}

setup(**config)
