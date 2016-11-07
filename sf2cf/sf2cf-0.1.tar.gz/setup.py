#!/usr/bin/env python3
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

def _install_reqs():
    with open('requirements.txt') as f:
        return f.read().split('\n')

setup(
    name='sf2cf',
    author="Cyril Roelandt",
    author_email="tipecaml@gmail.com",
    url="https://git.framasoft.org/Steap/sf2cf",
    version='0.1',
    description='Improve RSS/Atom feeds',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires = _install_reqs(),
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['sf2cf = sf2cf.sf2cf:main'],
        'sf2cf.feed': [
            'dilbert = sf2cf.feeds.dilbert:DilbertFeed',
            'cyanideandhappiness = sf2cf.feeds.cyanideandhappiness:CyanideAndHappinessFeed',
        ]
    },
)
