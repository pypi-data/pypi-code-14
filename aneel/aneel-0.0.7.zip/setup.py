# -*- coding: utf-8 -*-
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name="aneel",
      version="0.0.7",
      url="https://github.com/renatoefsousa/ANEEL",
      license="MIT License",
      author="Renato Eduardo Farias de Sousa",
      author_email="renato.ef.sousa@gmail.com",
      long_description=readme(),
      keywords="aneel calculations regulations",
      packages=["aneel"],
      description=u"This package performs various calculations related to ANEEL regulations.",
      install_requires=["csv", "json", "datetime"],
      include_package_data=True
)
