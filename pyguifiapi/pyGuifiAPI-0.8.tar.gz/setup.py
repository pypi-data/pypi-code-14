#!/usr/bin/env python

import sys
from setuptools import setup

#sys.path.insert(0, 'pyGuifiAPI')
from pyGuifiAPI import __version__ as VERSION
if sys.argv[-1] == 'publish':
    import os
    os.system("python setup.py sdist bdist_wheel upload -s")
    print("You probably want to also tag the version now:")
    print("  git tag -s -a v{version} -m 'version {version}'".format(version=VERSION))
    print("  git push --tags")
    sys.exit()


setup(
    name='pyGuifiAPI',
    packages=['pyGuifiAPI'],
    package_data={'': ['examples/*']},
    description="A Python interface for the Guifi.net API",
    long_description=open('README.md').read(),
    version=VERSION,
    author='Pablo Castellano',
    author_email='pablo@anche.no',
    url='https://github.com/PabloCastellano/pyGuifiAPI/',
    download_url='https://github.com/PabloCastellano/pyGuifiAPI/archive/master.zip',
    keywords=['free networks', 'guifi.net', 'API'],
    license='GPLv3+',
    data_files=[('', ['CHANGES.md', 'LICENSE.txt', 'README.md'])],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
