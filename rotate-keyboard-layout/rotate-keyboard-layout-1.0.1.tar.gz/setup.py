#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup
import sys

install_requires = []

if sys.version_info < (2, 7, 0):
    install_requires.append('argparse')

setup(
    name='rotate-keyboard-layout',
    version='1.0.1',
    author='Tarjei Husøy',
    author_email='git@thusoy.com',
    url='https://github.com/thusoy/rotate-keyboard-layout',
    description="Simple script to rotate among X keyboard layouts",
    py_modules=['rotate_keyboard_layout'],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'rotate-keyboard-layout = rotate_keyboard_layout:main',
        ]
    },
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment',
        'Topic :: Utilities',
    ],
)
