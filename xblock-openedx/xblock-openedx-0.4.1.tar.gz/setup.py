"""Set up for XBlock"""
from setuptools import setup

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'xblock/_version.py'
versioneer.versionfile_build = 'xblock/_version.py'
versioneer.tag_prefix = 'xblock-'  # tags are like 1.2.0
versioneer.parentdir_prefix = 'XBlock-'  # dirname like 'myproject-1.2.0'

setup(
    name='xblock-openedx',
    version='0.4.1',
    description='XBlock Core Library',
    author='Stanford OpenEdX',
    author_email='dev@lagunita.stanford.edu',
    url='https://github.com/Stanford-Online',
    packages=[
        'xblock',
        'xblock.django',
        'xblock.reference',
    ],
    install_requires=[
        'lxml',
        'markupsafe',
        'python-dateutil',
        'pytz',
        'webob',
    ],
    license='Apache 2.0',
)
