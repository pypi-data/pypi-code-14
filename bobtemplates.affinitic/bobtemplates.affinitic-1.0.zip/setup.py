# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '1.0'


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='bobtemplates.affinitic',
    version=version,
    description="Templates for Affinitic Plone projects.",
    long_description=long_description,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='web plone zope skeleton project',
    author='Affinitic',
    author_email='info@affinitic.be',
    url='https://github.com/affinitic/bobtemplates.affinitic',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['bobtemplates'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'mr.bob',
    ],
    extras_require={},
    entry_points={},
)
