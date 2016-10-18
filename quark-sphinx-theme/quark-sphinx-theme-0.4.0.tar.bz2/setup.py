#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from io import open
import os
import sys
from setuptools import setup, find_packages

dist_dir = os.path.dirname(os.path.abspath(__file__))
readme = os.path.join(dist_dir, 'README.rst')
with open(readme, 'r', encoding='utf-8') as f:
    long_description = f.read()

sys.path.insert(0, os.path.join(dist_dir, 'src', 'quark_sphinx_theme'))
from __version__ import __version__  # noqa
del sys.path[0]

setup(
    name='quark-sphinx-theme',
    version=__version__,
    description='A Sphinx theme designed for QTextBrowser',
    long_description=long_description,
    url='https://bitbucket.org/fk/quark-sphinx-theme',
    author='Felix Krull',
    author_email='f_krull@gmx.de',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Sphinx :: Theme',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],
    zip_safe=False,
    install_requires=['sphinx>=1.1'],
    python_requires='~=2.7, ~=3.3',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={
        'sphinx_themes': [
            'path = quark_sphinx_theme:get_path',
        ]
    },

    test_suite='test',
    tests_require=['html5lib', 'tinycss'],
)
