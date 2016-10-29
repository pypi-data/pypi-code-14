from setuptools import setup, find_packages
from os import path
import sys


here = path.abspath(path.dirname(__file__))

install_requires=[
    'arrow',
    'iso8601',
    'qiniu',
    'requests',
    'werkzeug',
]
if sys.version_info < (3, 5, 0):
    install_requires.append('typing')

setup(
    name='leancloud-sdk-ng',
    version='2.0.0',
    description='LeanCloud Python SDK',

    url='https://leancloud.cn/',

    author='ifanrx',
    author_email='ifanrx@ifanr.com',

    license='LGPL',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='Leancloud SDK',

    packages=find_packages(exclude=['docs', 'tests*']),

    test_suite='nose.collector',

    install_requires=install_requires,

    extras_require = {
        'dev': ['sphinx'],
        'test': ['nose', 'wsgi_intercept'],
    }
)
