import os
from setuptools import setup, find_packages


def readfile(filename, strip=False):
    with open(__path(filename), mode="rt") as f:
        rv = f.read()
    if strip:
        rv = rv.strip()
    return rv


def __path(filename):
    return os.path.join(os.path.dirname(__file__),
                        filename)


build = 6

if os.path.exists(__path('build.info')):
    build = open(__path('build.info')).read().strip()

version = '0.1.{}'.format(build)

setup(
    name="RQmargin",
    version=version,
    url="http://www.ricequant.com",
    author="ricequant",
    author_email="public@ricequant.com",
    description='fetch and store RQmargin data into mongodb.',
    packages=find_packages(exclude=[]),
    packages_data= {'RQmargin': ['config.json']},
    include_package_data=True,
    install_requires=["pandas",
                    "numpy",
                    "pymongo>=3.3.0",
                    "tushare>=0.5.0",
                    "typing"],
    zip_safe=False,


)
