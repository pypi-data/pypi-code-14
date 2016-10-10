import os
from setuptools import setup, find_packages

setup(
    name='kitch.data',
    version='0.0.1',
    description='A collection of data structures',
    long_description='A collection of data structures',
    url='https://github.com/j-kitch/data',
    author='Joshua Kitchen',
    author_email='joshdkitchen@gmail.com',
    liscense='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='data structures education linked list',
    packages=find_packages(exclude=['docs', 'tests'])
)
