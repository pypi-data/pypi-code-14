try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'digExtractor',
    'description': 'digExtractor',
    'author': 'Jason Slepicka',
    'url': 'https://github.com/usc-isi-i2/dig-extractor',
    'download_url': 'https://github.com/usc-isi-i2/dig-extractor',
    'author_email': 'jasonslepicka@gmail.com',
    'version': '0.1.7',
    # these are the subdirs of the current directory that we care about
    'packages': ['digExtractor'],
    'scripts': [],
    'install_requires':['jsonpath-rw>=1.4.0']
}

setup(**config)
