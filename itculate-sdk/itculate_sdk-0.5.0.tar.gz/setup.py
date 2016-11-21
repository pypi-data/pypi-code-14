from setuptools import setup
from os import path
from itculate_sdk import __version__

here = path.abspath(path.dirname(__file__))

setup(
    name="itculate_sdk",
    version=__version__,
    description="ITculate SDK",
    url="https://bitbucket.org/itculate/itculate-sdk",
    author="Ophir",
    author_email="opensource@itculate.io",
    license="MIT",
    keywords=["ITcualte", "sdk", "graph", "topology"],
    packages=["itculate_sdk", "itculate_sdk.api", "itculate_sdk.data_types", "itculate_sdk.upload"],
)
