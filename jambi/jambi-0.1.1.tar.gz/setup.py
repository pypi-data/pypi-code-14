#! /usr/bin/env python3
from setuptools import setup
from jambi.version import VERSION

setup(
    name='jambi',
    version=VERSION,
    url='https://www.github.com/kruchone/jambi',
    author='Zach Kruchoski',
    author_email='kruchone@gmail.com',
    description=('A peewee database migration manager'),
    long_description=(open('README.md').read()),
    license='MIT',
    packages=['jambi',],
    py_modules=['jambi',],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'jambi = jambi.jambi:main'
        ],
    },
    zip_safe=False,
    install_requires=[
        'peewee>=2.8.5',
        'psycopg2>=2.6.2',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
