#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import setup
from pip.req import parse_requirements
from pip.exceptions import InstallationError

from oshino_redis.version import get_version

try:
    install_reqs = list(parse_requirements("requirements.txt", session={}))
except InstallationError:
    # There are no requirements
    install_reqs = []

setup(name="oshino_redis",
      version=get_version(),
      description="...",
      author="zaibacu",
      packages=["oshino_redis"],
      install_requires=[str(ir.req) for ir in install_reqs],
      test_suite="pytest",
      tests_require=["pytest", "pytest-cov"],
      setup_requires=["pytest-runner"]
      )
