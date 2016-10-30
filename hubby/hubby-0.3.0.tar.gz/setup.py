#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re
import sys

install_requires = [
    'argcomplete',
    'requests',
]


version_file = os.path.join(os.path.dirname(__file__), 'hubby', '_version.py')
with open(version_file) as fh:
    version_file_contents = fh.read().strip()
    version_match = re.match(r"__version__ = '(\d\.\d.\d.*)'", version_file_contents)
    version = version_match.group(1)


setup(
    name='hubby',
    version=version,
    author='Tarjei Husøy',
    author_email='git@thusoy.com',
    url='https://github.com/thusoy/hubby',
    description="Hub alternatives",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'git-assignees = hubby.cli:list_assignees',
            'git-pull-request = hubby.cli:create_or_update_pull_request',
        ]
    },
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        # 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
)
