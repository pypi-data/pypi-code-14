from codecs import open
from os import environ, path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

try:
    snapshot = 'dev%s' % environ['BUILD_NUMBER']
except KeyError:
    snapshot = ''

setup(
    name='rds-snapshot',

    version='0.1.1%s' % snapshot,

    description='A tool for handling RDS snapshots in AWS from the CLI or in scripts.',
    long_description=long_description,

    url='https://github.com/elias5000/rds-snapshot',

    author='Frank Wittig',
    author_email='frank@e5k.de',

    license='Apache License, Version 2',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Environment :: Console',

        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',

        'License :: OSI Approved :: Apache Software License',

        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',

        'Topic :: System :: Archiving :: Backup',
        'Topic :: Utilities'
    ],

    keywords='aws rds snapshots',

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rds-snapshot=rds_snapshot:main'
        ]
    },

    install_requires=['boto3']
)
