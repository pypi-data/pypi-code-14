import codecs
import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
requirement_file = os.path.join(here, 'requirements.txt')


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open(requirement_file, 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

setup(name="redis-cluster-backend",
      version=find_version('redis_cluster_backend', '__init__.py'),
      description="redis cluster backend for celery",
      license="MIT",
      author="Ryan Kung",
      author_email="ryankung@ieee.org",
      install_requires=requires,
      url="http://github.com/ryankung/celery-redis-cluster-backend",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Operating System :: OS Independent",
          "Topic :: Software Development",
          "Topic :: Software Development :: Libraries :: Python Modules"
      ],
      py_modules=find_packages(exclude=['tests', 'docs']),
      packages=find_packages(exclude=['tests', 'docs']),
      keywords="celery redis cluster backend",
      zip_safe=True)
