from setuptools import setup, find_packages

config = {
    'name': 'landmark_ml',
    'description': 'Machine learning library for the landmark set of tools',
    'author': 'InferLink',
    'url': 'https://github.com/inferlink/landmark-ml',
    'download_url': 'https://github.com/inferlink/landmark-ml',
    'author_email': 'developers@inferlink.com ',
    'version': '0.1',
    'license': 'GNU AGPL',
    'packages': find_packages(),
    'classifiers': []
}

setup(**config)