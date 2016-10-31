# -*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

def read_file(filename):
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''

install_requires = [
    'mercurial>=3.9.2',
    ]


setup(name='hg_api',
      version='0.1.0',
      description='A simple api interact with mercurial',
      long_description=read_file('README.rst'),
      classifiers=[
          "Programming Language :: Python",
      ],
      author='yafeile',
      author_email='yafeile@sohu.com',
      url='https://bitbucket.org/yafeile/hg_api',
      keywords='hg',
      packages=find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests"
        ]),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      )
