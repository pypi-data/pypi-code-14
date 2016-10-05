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
    'version': '0.2.0',
    # these are the subdirs of the current directory that we care about
    'packages': ['digReadabilityExtractor', 'digReadabilityExtractor.readability'],
    'scripts': [],
    'install_requires': ['digExtractor>=0.2.0','lxml>=3.6.0','beautifulsoup4>=4.3','cssselect','chardet']
}

setup(**config)
