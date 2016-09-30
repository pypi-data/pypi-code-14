from setuptools import setup
from setuptools import find_packages

from pypandoc import convert_file


setup(
    name='talkzoho',
    version='0.9.6',
    description='Asynchronous wrapper for Zoho\'s numerous APIs',
    long_description=convert_file('README.md', 'rst'),
    url='https://github.com/A2Z-Cloud/Talk-Zoho',
    packages=find_packages(exclude=('tests', 'tests.*')),
    author='James Stidard',
    author_email='james.stidard@a2zcloud.com',
    keywords=['talkzoho', 'Zoho', 'async', 'tornado'],
    install_requires=[
        'fuzzywuzzy',
        'python-Levenshtein',
        'tornado'])
