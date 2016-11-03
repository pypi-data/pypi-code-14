#! /usr/bin/env python
#! -*- coding: utf-8 *-*-

from setuptools import setup, find_packages

readme = open('README.md', 'r').read()
setup(
    name='mpx',
    version='0.1',
    url='https://github.com/khilnani/mpx',
    license='MIT',
    author='khilnani',
    author_email='nik@khilnani.org',
    description='Python client for thePlatform MPX API.',
    include_package_data=True,
    long_description=readme,
    packages=find_packages(),
    install_requires=['requests','texttable'],
    keywords=('mpx', 'thePlatform', 'pdk'),
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Multimedia :: Video',

    ],  
    ) 
