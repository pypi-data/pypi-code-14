#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='rigid',
    version='0.2.1',
    description='Rig up your web application in seconds',
    url='https://rigidapp.com/',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rigid = rigid.commands:cli',
        ]
    },
    install_requires=[
        'click',
        'requests',
        'pyyaml',
    ],
    tests_require=['six'],
    author='Kyle Fuller',
    author_email='kyle@cocode.org',
    license='BSD',
    classifiers=(
      'Development Status :: 5 - Production/Stable',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5',
      'License :: OSI Approved :: BSD License',
    )
)
