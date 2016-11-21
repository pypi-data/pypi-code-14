# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from moven import __version__

_description = "machine/deep learning model distribution relying on Maven infrastructure"
try:
    _long_description = open('README.md').read()
except IOError:
    _long_description = _description  # TODO

try:
    with open('requirements.txt', 'r') as f:
        _install_requires = [line.rstrip('\n') for line in f]
except IOError:
    _install_requires = []  # TODO
    
setup(
    name="moven",
    version=__version__,
    author="Sergio Fernández",
    author_email="sergio.fernandez@redlink.co",
    description=_description,
    packages=['moven'],
    long_description=_long_description,
    platforms=['any'],
    install_requires=_install_requires,
    entry_points={
        'console_scripts': [
            'moven = moven.moven:main'
        ]
    },
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Topic :: Software Development :: Build Tools',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Java',
                 'Environment :: Console'],
    keywords='python ml models maven',
    use_2to3=True
)
