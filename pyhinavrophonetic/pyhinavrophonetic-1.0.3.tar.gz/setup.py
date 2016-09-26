#!/usr/bin/env python

try:
    from setuptools import setup
    from pyhinavrophonetic import __version__


    setup(name='pyhinavrophonetic',
          version='1.0.0',
          description='Python implementation to convert phonetic to hindi',
          long_description=open('README.rst', 'rt').read(),
          author='Subrata Sarkar',
          author_email='subrotosarkar32@gmail.com',
          url='https://bitbucket.org/SubrataSarkar32/pyhinavrophonetic/',
          packages=['pyhinavrophonetic','pyhinavrophonetic.utils'],
          package_data = {'pyhinavrophonetic': ['*.rst', 'resources/*.json','utils/resources/*.json']},
          include_package_data = True,
          install_requires=["simplejson >= 3.0.0"],
          license='GNU GPL v3 or later',
          classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            ]
          )

except ImportError:
    print 'Install setuptools'
