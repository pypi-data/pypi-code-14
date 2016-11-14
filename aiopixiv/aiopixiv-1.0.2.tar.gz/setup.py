import sys

if sys.version_info[0:2] < (3, 5):
    raise Exception("aiopixiv requires Python 3.5+")

from setuptools import setup
from aiopixiv import __version__

setup(
    name='aiopixiv',
    version=__version__,
    packages=['aiopixiv'],
    url='https://github.com/SunDwarf/aiopixiv',
    license='MIT',
    author='Isaac Dickinson',
    author_email='sun@veriny.tf',
    description='An asyncio wrapper for the Pixiv API.',
    install_requires=[
        "aiohttp>=1.0.0,<=1.1.0"
    ]
)
