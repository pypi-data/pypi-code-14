from setuptools import setup
from setuptools import find_packages


setup(
    name='talkzoho',
    version='0.9.5',
    description='Asynchronous wrapper for Zoho\'s numerous APIs',
    url='https://github.com/A2Z-Cloud/Talk-Zoho',
    packages=find_packages(exclude=('tests', 'tests.*')),
    author='James Stidard',
    author_email='james.stidard@a2zcloud.com',
    install_requires=[
        'fuzzywuzzy',
        'python-Levenshtein',
        'tornado'])
