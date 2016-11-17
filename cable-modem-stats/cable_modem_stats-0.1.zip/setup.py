#!/usr/bin/env python

from setuptools import setup


requires = [
    'beautifulsoup4',
    'requests',
    'six',
]

setup(
    name='cable_modem_stats',
    version='0.1',
    packages=[
        'cable_modem_stats',
        'cable_modem_stats.stats',
        'cable_modem_stats.models',
    ],
    install_requires=requires,
    scripts=[
        'scripts/modem-stats.py',
    ],
    url='https://bitbucket.org/phistrom/cable_modem_stats',
    license='Apache 2.0',
    author='Phillip Stromberg',
    author_email='phillip+cable_modem_stats@stromberg.me',
    description="Pull stats from compatible cable modem's web interfaces to monitor SNR, Power, etc.",
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Networking :: Monitoring',
    ),
)
