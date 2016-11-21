from setuptools import setup, find_packages
from os import path
import itculate_sdk

here = path.abspath(path.dirname(__file__))

setup(
    name="itculate_sdk",
    version=itculate_sdk.__version__,
    description="ITculate SDK",
    url="https://bitbucket.org/itculate/itculate-sdk",
    author="Ophir",
    author_email="opensource@itculate.io",
    license="MIT",
    keywords=["ITcualte", "sdk", "graph", "topology"],
    package_data={'itculate_sdk/*': ['*.csv']},
    packages=find_packages(),
)
