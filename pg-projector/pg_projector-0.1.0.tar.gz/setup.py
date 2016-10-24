#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pg_projector',
    version='0.1.0',
    description="The PostGIS Projector provides an SQLAlchemy module to describe and interact with the 'spatial_ref_sys' table in PostGIS.",
    long_description=readme,
    author='Daven Quinn',
    author_email='daven@davenquinn.com',
    url='https://github.com/davenquinn/pg_projector',
    packages=[
        'pg_projector',
    ],
    package_dir={'pg_projector':
                 'pg_projector'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pg_projector',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
