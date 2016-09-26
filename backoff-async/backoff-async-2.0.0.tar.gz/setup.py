# coding:utf-8

import backoff

from distutils import core


classifiers = ['Development Status :: 5 - Production/Stable',
               'Intended Audience :: Developers',
               'Programming Language :: Python',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: Implementation',
               'Programming Language :: Python :: Implementation :: CPython',
               'Topic :: Internet :: WWW/HTTP',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: Utilities']


def readme():
    with open("README.rst", "r") as infile:
        return infile.read()


core.setup(name='backoff-async',
           version='2.0.0',
           description="Function decoration for backoff and retry async functions",
           long_description=readme(),
           py_modules=['backoff'],
           author="Bob Green, Alexandr Skurikhin",
           author_email="bgreen@litl.com, a.skurihin@gmail.com",
           keywords = "backoff function decorator async",
           url="https://github.com/a.sk/backoff-async",
           license="MIT",
           classifiers=classifiers)
